import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot(PlotType.Cartesian3D).show_isosurfaces=True
tp.active_frame().plot().isosurface(0).definition_contour_group_index=1
tp.active_frame().plot().isosurface(0).isosurface_values[0]=-6000

tp.active_frame().plot().isosurface(0).contour.flood_contour_group_index=0
tp.active_frame().plot().slice(0).effects.use_translucency=True
tp.active_frame().plot().slice(0).effects.surface_translucency=40

tp.active_frame().plot().view.psi=68.2286
tp.active_frame().plot().view.theta=-124.114
tp.active_frame().plot().view.position=(
    2.95931,
    tp.active_frame().plot().view.position[1],
    tp.active_frame().plot().view.position[2])
tp.active_frame().plot().view.position=(
    tp.active_frame().plot().view.position[0],
    2.15999,
    tp.active_frame().plot().view.position[2])
tp.active_frame().plot().view.position=(
    tp.active_frame().plot().view.position[0],
    tp.active_frame().plot().view.position[1],
    1.45886)
tp.active_frame().plot().view.width=0.339885
# End Macro.
