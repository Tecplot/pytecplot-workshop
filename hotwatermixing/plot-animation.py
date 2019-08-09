import glob
import os
import re
import sys

import tecplot as tp
from tecplot.constant import *


def plot_data(plot):
    T = plot.frame.dataset.variable('Temperature')
    P = plot.frame.dataset.variable('Pressure')

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


if '-c' in sys.argv:
    tp.session.connect()

# sorting on filenames determines order of animation
files = sorted(glob.glob('HotWaterMixing_Y05YT10*.plt'))

# clear the layout, load the data and activate the 3D plot
tp.new_layout()
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
    for zone in dataset.zones('fluid'):
        fmap = plot.fieldmap(zone)
        fmap.show = True
        animation.export_animation_frame()
        fmap.show = False
