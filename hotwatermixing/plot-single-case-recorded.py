import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.macro.execute_command("""$!ReadDataSet  '\"/home/john/workspace/workshops/2019.8-tfaws/data/hotwatermixing/HotWaterMixing.plt\" '
  ReadDataOption = New
  ResetStyle = No
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '\"X\" \"Y\" \"Z\" \"Pressure\" \"X Velocity\" \"Y Velocity\" \"Z Velocity\" \"Temperature\" \"Turbulent Viscosity\"'""")
tp.active_frame().plot().rgb_coloring.red_variable_index=3
tp.active_frame().plot().rgb_coloring.green_variable_index=3
tp.active_frame().plot().rgb_coloring.blue_variable_index=3
tp.active_frame().plot().contour(0).variable_index=3
tp.active_frame().plot().contour(1).variable_index=4
tp.active_frame().plot().contour(2).variable_index=5
tp.active_frame().plot().contour(3).variable_index=6
tp.active_frame().plot().contour(4).variable_index=7
tp.active_frame().plot().contour(5).variable_index=8
tp.active_frame().plot().contour(6).variable_index=3
tp.active_frame().plot().contour(7).variable_index=3
tp.active_frame().plot(PlotType.Cartesian3D).show_slices=True
tp.active_frame().plot().show_shade=False
tp.macro.execute_command('''$!Pick SetMouseMode
  MouseMode = Select''')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 9.02285714286
  Y = 3.70357142857
  ConsiderStyle = Yes''')
tp.active_frame().plot().contour(0).legend.auto_resize=True
tp.active_frame().plot().contour(0).variable_index=7
tp.active_frame().plot().contour(0).colormap_filter.distribution=ColorMapDistribution.Continuous
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 8.89428571429
  Y = 3.49785714286
  ConsiderStyle = Yes''')
tp.active_frame().plot().contour(0).colormap_filter.continuous_min=280
tp.active_frame().plot().contour(0).colormap_filter.continuous_max=380
# End Macro.
