import sys

import numpy as np

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# if "-c" is passed as an argument from the
# console conntect to Tecplot 360 on the
# default port (7600) and clear the layout
if '-c' in sys.argv:
    tp.session.connect()
    tp.new_layout()

# load a single data file
infile = 'hotwatermixing/HotWaterMixing.plt'
dataset = tp.data.load_tecplot(infile)

# get handles to variables in the dataset
T = dataset.variable('Temperature')
P = dataset.variable('Pressure')

# get handle to 3D plot
plot = tp.active_frame().plot(PlotType.Cartesian3D)

# turn on slices and isosurfaces, turn off shade
plot.show_shade = False
plot.show_slices = True
plot.show_isosurfaces = True

# set slice flood contour to Temperature
# and adjust contour levels
contour = plot.slice(0).contour.flood_contour_group
contour.variable = T
contour.legend.auto_resize = True
contour.levels.reset_levels(np.linspace(280, 380, 201))

# get handle to isosurface group
isosurf = plot.isosurface(0)

# isosurface will be a constant value of Pressure
isosurf.definition_contour_group_index = 1
isosurf.definition_contour_group.variable = P
isosurf.isosurface_values = -6000

# isosurface contoured by Temperature
isosurf.contour.flood_contour_group = contour

# make slice translucent
slice = tp.active_frame().plot().slice(0)
slice.effects.use_translucency = True
slice.effects.surface_translucency = 40

# adjust the view
plot.view.psi = 68.2286
plot.view.theta = -124.114
plot.view.position = 2.95931, 2.15999, 1.45886
plot.view.width = 0.339885

# save image
tp.save_png('hotwater-isosurface.png')

