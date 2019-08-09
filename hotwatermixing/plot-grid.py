import glob
import os
import re
import sys

import tecplot as tp
from tecplot.constant import *


def plot_data(frame, infile):
    dataset = tp.data.load_tecplot(infile, frame=frame)
    frame.activate()
    T = dataset.variable('Temperature')
    P = dataset.variable('Pressure')

    plot = frame.plot(PlotType.Cartesian3D)

    contour = plot.contour(0)
    contour.variable = T
    contour.legend.auto_resize = True
    contour.colormap_filter.distribution = \
        ColorMapDistribution.Continuous
    contour.colormap_filter.continuous_min = 280
    contour.colormap_filter.continuous_max = 380

    isosurf = tp.active_frame().plot().isosurface(0)
    isosurf.definition_contour_group_index = 1
    isosurf.definition_contour_group.variable = P
    isosurf.contour.flood_contour_group = contour
    isosurf.isosurface_values = -6000

    slice = tp.active_frame().plot().slice(0)
    slice.effects.use_translucency = True
    slice.effects.surface_translucency = 40

    plot.show_shade = False
    plot.show_slices = True
    plot.show_isosurfaces = True

    plot.view.psi = 68.2286
    plot.view.theta = -124.114
    plot.view.position = 2.95931, 2.15999, 1.45886
    plot.view.width = 0.339885


def frame_grid(nrows, ncols):
    scale = max(nrows, ncols)
    page = tp.add_page()
    frames = []
    for row in range(nrows):
        frame_row = []
        for col in range(ncols):
            if row or col:
                frame = page.add_frame()
            else:
                frame = page.active_frame()
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

files = sorted(glob.glob('HotWaterMixing_Y05YT10*.plt'))
pattern = re.compile(r'Z(\d+)ZT(\d+)')

filename = 'HotWaterMixing_Y05YT10Z{:0>2}ZT{:0>3}.plt'

Z, ZT = zip(*[[int(x)
               for x in pattern.search(f).groups()]
              for f in files])
Z = sorted(set(Z))
ZT = sorted(set(ZT))

frames = frame_grid(len(ZT), len(Z))

for zt, frame_row in zip(ZT, frames):
    for z, frame in zip(Z, frame_row):
        fname = filename.format(z, zt)
        if os.path.exists(fname):
            plot_data(frame, fname)

tp.save_png('hotwater-grid.png')
