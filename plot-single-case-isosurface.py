import sys
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

if '-c' in sys.argv:
    tp.session.connect()
    tp.new_layout()

infile = 'HotWaterMixing.plt'
dataset = tp.data.load_tecplot(infile)
T = dataset.variable('Temperature')
P = dataset.variable('Pressure')

frame = tp.active_frame()
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

tp.save_png('hotwater-isosurface.png')
