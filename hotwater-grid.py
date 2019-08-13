import glob
import os
import re
import sys

import numpy as np

import tecplot as tp
from tecplot.constant import *

def plot_data(datafile, frame):
    """Plot Isosurface of constant Pressure, contouring on Temperature"""
    with frame.activated():
        tp.data.load_tecplot(datafile)
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()
        plot.show_shade = False
        plot.show_slices = True
        plot.show_isosurfaces = True
        contour = plot.slice(0).contour.flood_contour_group
        contour.variable = frame.dataset.variable('Temperature')
        contour.legend.auto_resize = True
        contour.levels.reset_levels(np.linspace(280, 380, 201))
        isosurf = plot.isosurface(0)
        isosurf.definition_contour_group_index = 1
        isosurf.definition_contour_group.variable = frame.dataset.variable('Pressure')
        isosurf.isosurface_values = -6000
        isosurf.contour.flood_contour_group = contour
        slice = frame.plot().slice(0)
        slice.effects.use_translucency = True
        slice.effects.surface_translucency = 40
        plot.view.psi = 68.2286
        plot.view.theta = -124.114
        plot.view.position = 2.95931, 2.15999, 1.45886
        plot.view.width = 0.339885

def frame_grid(nrows, ncols):
    scale = max(nrows, ncols)
    frames = []
    for row in range(nrows):
        frame_row = []
        for col in range(ncols):
            if row or col:
                frame = tp.active_page().add_frame()
            else:
                frame = tp.active_page().active_frame()
            pos = (scale * col / ncols,
                   scale * (1 - row / nrows))
            height = scale / nrows
            width = scale / ncols
            frame.position = pos
            frame.height = height
            frame.width = width
            frame_row.append(frame)
        frames.append(frame_row)
    tp.macro.execute_command('$!WorkspaceView FitAllFrames')
    return frames

if '-c' in sys.argv:
    tp.session.connect()
    tp.new_layout()

# get list of input data files
files = sorted(glob.glob('hotwatermixing/HotWaterMixing_Y05YT10*.plt'))

# setup regular expression to extract input velocity (Z) and temperature (ZT)
pattern = re.compile(r'Z(\d+)ZT(\d+)')

# filename format
filename = 'hotwatermixing/HotWaterMixing_Y05YT10Z{:0>2}ZT{:0>3}.plt'

# get sorted values of input velocity (Z) and temperature (ZT)
Z, ZT = zip(*[[int(x)
               for x in pattern.search(f).groups()]
              for f in files])
Z = sorted(set(Z))
ZT = sorted(set(ZT))

# create grid of frames
frames = frame_grid(len(ZT), len(Z))

# in each frame, load data and adjust plot style
for zt, frame_row in zip(ZT, frames):
    for z, frame in zip(Z, frame_row):
        datafile = filename.format(z, zt)
        if os.path.exists(datafile):
            plot_data(datafile, frame)

tp.save_png('hotwater-grid.png')

