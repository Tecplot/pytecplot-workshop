import sys
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

if '-c' in sys.argv:
    tp.session.connect()
    tp.new_layout()

infile = 'HotWaterMixing.plt'
dataset = tp.data.load_tecplot(infile)

frame = tp.active_frame()
plot = frame.plot(PlotType.Cartesian3D)
plot.show_slices = True
plot.show_shade = False

contour = plot.contour(0)

contour.variable = dataset.variable('Temperature')
contour.legend.auto_resize = True
contour.colormap_filter.distribution = \
    ColorMapDistribution.Continuous
contour.colormap_filter.continuous_min = 280
contour.colormap_filter.continuous_max = 380

tp.save_png('hotwater-slice.png')
