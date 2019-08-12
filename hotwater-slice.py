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

# get handle to the 3D plot in the active frame
plot = tp.active_frame().plot(PlotType.Cartesian3D)

# turn off shade
plot.show_shade = False

# turn on slices
plot.show_slices = True

# get the contour group from the slice group
contour = plot.slice(0).contour.flood_contour_group

# set contour variable
contour.variable = dataset.variable('Temperature')

# adjust legend properties
contour.legend.auto_resize = True

# set contour levels
contour.levels.reset_levels(np.linspace(280, 380, 201))

# save image of slice through pipe
tp.save_png('hotwater-slice.png')

