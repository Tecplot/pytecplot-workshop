import sys

import numpy as np
from scipy import interpolate, optimize, stats


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

# create a slice at the exit point of the pipe
pipe_exit = tp.data.extract.extract_slice((0, 0.34, 0), (0, 1, 0))

# get y-velocity on this slice
x = pipe_exit.values('X')[:]
z = pipe_exit.values('Z')[:]
vy = pipe_exit.values('Y Velocity')[:]

def velocity_model(xy, a, b):
    x, y = xy
    return a * (x**2 + y**2) + b

# fit data to our model
pfit, pcov = optimize.curve_fit(velocity_model, (x, z), vy, p0=[1, 1])
perr = np.sqrt(np.abs(pcov.diagonal()))

# chi-sq test for the fit
ndf = len(vy) - len(pfit)
vy_fit = velocity_model((x, z), *pfit)
chisq, pval = stats.chisquare(vy, vy_fit, len(pfit))

print(f'''\
y-velocity equation: a * (x**2 + y**2) + b
fitted parameters:
    a: {pfit[0]:.3f} +/- {perr[0]:.3f}
    b: {pfit[1]:.3f} +/- {perr[1]:.3f}
    chi-sq / ndf: {chisq/ndf:.3f}''')


t = pipe_exit.values('Temperature')[:]
print(f'''\
temperature:
    average: {np.average(t)}
    stddev: {np.std(t)}''')

def velocity_model(xy, x0, y0, a, b):
    x, y = xy
    return a * ((x - x0)**2 + (y - y0)**2) + b

# fit data to our model
pfit, pcov = optimize.curve_fit(velocity_model, (x, z), vy, p0=[0, 0, 1, 1])
perr = np.sqrt(np.abs(pcov.diagonal()))

# chi-sq test for the fit
ndf = len(vy) - len(pfit)
vy_fit = velocity_model((x, z), *pfit)
chisq, pval = stats.chisquare(vy, vy_fit, len(pfit))
print(f'''\
y-velocity equation: a * ((x - x0)**2 + (y - y0)**2) + b
fitted parameters:
    x0: {pfit[0]:.3f} +/- {perr[0]:.3f}
    y0: {pfit[1]:.3f} +/- {perr[1]:.3f}
    a: {pfit[2]:.3f} +/- {perr[2]:.3f}
    b: {pfit[3]:.3f} +/- {perr[3]:.3f}
    chi-sq / ndf: {chisq/ndf:.3f}''')


"""



xx = np.linspace(x.min(), x.max(), 300)
zz = np.linspace(z.min(), z.max(), 300)
X, Z = np.meshgrid(xx, zz)
Vdata = interpolate.griddata((x, z), vy, (X, Z))
Vfit = velocity_model((X, Z), *pfit)

from matplotlib import pyplot
fig, ax = pyplot.subplots(2,2)
for ax, data in zip(ax.ravel(), (Vfit, Vdata, Vdata - Vfit)):
    plt = ax.pcolormesh(X, Z, data)
    fig.colorbar(plt, ax=ax)
pyplot.show()


# Calculate cell area (using cell volume calculation from CFDA)
tp.macro.execute_extended_command('CFDAnalyzer4', r'''
    Calculate Function='CELLVOLUME'
    Normalization='None'
    ValueLocation='CellCentered'
    CalculateOnDemand='F'
    UseMorePointsForFEGradientCalculations='F'
''')

# calculate cell-centered temperature and velocity
tp.data.operate.execute_equation(
    '{Temperature CC}={Temperature}',
    value_location=ValueLocation.CellCentered)
tp.data.operate.execute_equation(
    '{Y Velocity CC}={Y Velocity}',
    value_location=ValueLocation.CellCentered)

# fetch data from Tecplot into Python
cellvol = pipe_exit.values('Cell Volume')[:]
temp = pipe_exit.values('Temperature CC')[:]
yvel = pipe_exit.values('Y Velocity CC')[:]

# normalize cell volume so the sum is equal to one
cellvol /= np.sum(cellvol)

# calculate average velocity and temperature
avgyvel = np.sum(yvel * cellvol)
avgtemp = np.sum(temp * cellvol)
print(f'average velocity: {avgyvel}')
print(f'average temperature: {avgtemp}')

# calculate the standard deviate of velocity and temperature
stddev_yvel = np.std(yvel)
stddev_temp = np.std(temp)
print(f'stddev velocity: {stddev_yvel}')
print(f'stddev temperature: {stddev_temp}')

stddev_yvel = np.std(yvel * cellvol / np.sum(cellvol))
stddev_temp = np.std(temp * cellvol / np.sum(cellvol))
print(f'stddev velocity: {stddev_yvel}')
print(f'stddev temperature: {stddev_temp}')

"""

