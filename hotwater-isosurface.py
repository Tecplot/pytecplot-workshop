import sys
import numpy as np
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

if '-c' in sys.argv:
    tp.session.connect()
    tp.new_layout()

infile = 'hotwatermixing/HotWaterMixing.plt'
dataset = tp.data.load_tecplot(infile)
plot = tp.active_frame().plot(PlotType.Cartesian3D)
plot.show_shade = False
plot.show_slices = True
contour = plot.slice(0).contour.flood_contour_group
contour.variable = dataset.variable('Temperature')
contour.legend.auto_resize = True
contour.levels.reset_levels(np.linspace(280, 380, 201))

# get handle to isosurface group
isosurf = plot.isosurface(0)

isosurf.definition_contour_group_index = 1
isosurf.definition_contour_group.variable = P
isosurf.contour.flood_contour_group = contour
isosurf.isosurface_values = -6000

slice = tp.active_frame().plot().slice(0)
slice.effects.use_translucency = True
slice.effects.surface_translucency = 40


plot.view.psi = 68.2286
plot.view.theta = -124.114
plot.view.position = 2.95931, 2.15999, 1.45886
plot.view.width = 0.339885

tp.save_png('hotwater-isosurface.png')

