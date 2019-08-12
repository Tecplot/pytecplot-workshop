import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.macro.execute_command("""$!ReadDataSet  '\"hotwatermixing/HotWaterMixing.plt\" '
  ReadDataOption = New
  ResetStyle = No
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '\"X\" \"Y\" \"Z\" \"Pressure\" \"X Velocity\" \"Y Velocity\" \"Z Velocity\" \"Temperature\" \"Turbulent Viscosity\"'""")
tp.macro.execute_command('$!GlobalRGB RedChannelVar = 4')
tp.macro.execute_command('$!GlobalRGB GreenChannelVar = 4')
tp.macro.execute_command('$!GlobalRGB BlueChannelVar = 4')
tp.active_frame().plot().contour(0).variable_index=3
tp.active_frame().plot().contour(1).variable_index=4
tp.active_frame().plot().contour(2).variable_index=5
tp.active_frame().plot().contour(3).variable_index=6
tp.active_frame().plot().contour(4).variable_index=7
tp.active_frame().plot().contour(5).variable_index=8
tp.active_frame().plot().contour(6).variable_index=3
tp.active_frame().plot().contour(7).variable_index=3
tp.active_frame().plot(PlotType.Cartesian3D).show_shade=False
tp.active_frame().plot().show_slices=True
tp.active_frame().plot().slice(0).contour.flood_contour_group_index=4
tp.active_frame().plot().contour(4).levels.reset_levels([280, 280.503, 281.005, 281.508, 282.01, 282.513, 283.015, 283.518, 284.02, 284.523, 285.025, 285.528, 286.03, 286.533, 287.035, 287.538, 288.04, 288.543, 289.045, 289.548, 290.05, 290.553, 291.055, 291.558, 292.06, 292.563, 293.065, 293.568, 294.07, 294.573, 295.075, 295.578, 296.08, 296.583, 297.085, 297.588, 298.09, 298.593, 299.095, 299.598, 300.101, 300.603, 301.106, 301.608, 302.111, 302.613, 303.116, 303.618, 304.121, 304.623, 305.126, 305.628, 306.131, 306.633, 307.136, 307.638, 308.141, 308.643, 309.146, 309.648, 310.151, 310.653, 311.156, 311.658, 312.161, 312.663, 313.166, 313.668, 314.171, 314.673, 315.176, 315.678, 316.181, 316.683, 317.186, 317.688, 318.191, 318.693, 319.196, 319.698, 320.201, 320.704, 321.206, 321.709, 322.211, 322.714, 323.216, 323.719, 324.221, 324.724, 325.226, 325.729, 326.231, 326.734, 327.236, 327.739, 328.241, 328.744, 329.246, 329.749, 330.251, 330.754, 331.256, 331.759, 332.261, 332.764, 333.266, 333.769, 334.271, 334.774, 335.276, 335.779, 336.281, 336.784, 337.286, 337.789, 338.291, 338.794, 339.296, 339.799, 340.302, 340.804, 341.307, 341.809, 342.312, 342.814, 343.317, 343.819, 344.322, 344.824, 345.327, 345.829, 346.332, 346.834, 347.337, 347.839, 348.342, 348.844, 349.347, 349.849, 350.352, 350.854, 351.357, 351.859, 352.362, 352.864, 353.367, 353.869, 354.372, 354.874, 355.377, 355.879, 356.382, 356.884, 357.387, 357.889, 358.392, 358.894, 359.397, 359.899, 360.402, 360.905, 361.407, 361.91, 362.412, 362.915, 363.417, 363.92, 364.422, 364.925, 365.427, 365.93, 366.432, 366.935, 367.437, 367.94, 368.442, 368.945, 369.447, 369.95, 370.452, 370.955, 371.457, 371.96, 372.462, 372.965, 373.467, 373.97, 374.472, 374.975, 375.477, 375.98, 376.482, 376.985, 377.487, 377.99, 378.492, 378.995, 379.497, 380])
tp.macro.execute_command('$!RedrawAll')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 8.3804664723
  Y = 3.29373177843
  ConsiderStyle = Yes''')
tp.active_frame().plot().contour(4).legend.auto_resize=True
tp.macro.execute_command('$!RedrawAll')
# End Macro.

