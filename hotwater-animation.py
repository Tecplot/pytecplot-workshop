import glob
import sys

import numpy as np

import tecplot as tp
from tecplot.constant import *

def plot_data(plot):
    """Plot Isosurface of constant Pressure, contouring on Temperature"""
    T = plot.frame.dataset.variable('Temperature')
    P = plot.frame.dataset.variable('Pressure')
    plot = tp.active_frame().plot(PlotType.Cartesian3D)
    plot.show_shade = False
    plot.show_slices = True
    plot.show_isosurfaces = True
    contour = plot.slice(0).contour.flood_contour_group
    contour.variable = T
    contour.legend.auto_resize = True
    contour.levels.reset_levels(np.linspace(280, 380, 201))
    isosurf = plot.isosurface(0)
    isosurf.definition_contour_group_index = 1
    isosurf.definition_contour_group.variable = P
    isosurf.isosurface_values = -6000
    isosurf.contour.flood_contour_group = contour
    slice = tp.active_frame().plot().slice(0)
    slice.effects.use_translucency = True
    slice.effects.surface_translucency = 40
    plot.view.psi = 68.2286
    plot.view.theta = -124.114
    plot.view.position = 2.95931, 2.15999, 1.45886
    plot.view.width = 0.339885

if '-c' in sys.argv:
    tp.session.connect()
    tp.new_layout()

# sorting on filenames determines order of animation
files = sorted(glob.glob('hotwatermixing/HotWaterMixing_Y05YT10*.plt'))

# load all data files and activate the 3D plot
dataset = tp.data.load_tecplot(files)
plot = tp.active_frame().plot(PlotType.Cartesian3D)
plot.activate()

# setup plot style
plot_data(plot)

# Turn all fieldmaps off
for fmap in plot.fieldmaps():
    fmap.show = False

# Turn on one fieldmap at a time and save animation frame
with tp.export.animation_mpeg4('hotwater-animation.mpg') as animation:

    # for each zone named "fluid"
    # these will be in the order they were loaded
    for zone in dataset.zones('fluid'):

        # get handle to fieldmap for this zone
        fmap = plot.fieldmap(zone)

        # turn on this fieldmap
        fmap.show = True

        # export a single animation frame
        animation.export_animation_frame()

        # turn off this fieldmap
        fmap.show = False

