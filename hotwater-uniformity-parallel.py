import atexit
import glob
import os
import multiprocessing
import re

import numpy as np
from scipy import optimize, stats

import tecplot as tp

def init():
    # !!! IMPORTANT !!!
    # Must register stop at exit to ensure Tecplot cleans
    # up all temporary files and does not create a core dump
    atexit.register(tp.session.stop)

def work(datafile):
    match = re.search(r'Z(\d+)ZT(\d+)', datafile)
    Z, ZT = int(match.group(1)), int(match.group(2))
    tp.new_layout()
    tp.data.load_tecplot(datafile)

    # create a slice at the exit point of the pipe
    pipe_exit = tp.data.extract.extract_slice((0, 0.3, 0), (0, 1, 0))

    # get y-velocity on this slice
    x = pipe_exit.values('X')[:]
    z = pipe_exit.values('Z')[:]
    vy = pipe_exit.values('Y Velocity')[:]
    t = pipe_exit.values('Temperature')[:]

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

    def velocity_model(xy, x0, y0, a, b):
        x, y = xy
        return a * ((x - x0)**2 + (y - y0)**2) + b

    # fit data to our model
    pfit, pcov = optimize.curve_fit(velocity_model, (x, z), vy, p0=[0, 0, 1, 1])
    y0 = pfit[1]

    return Z, ZT, chisq/ndf, np.std(vy), np.std(t), y0

if __name__ == '__main__':
    # !!! IMPORTANT !!!
    # On Linux systems, Python's multiprocessing start method
    # defaults to "fork" which is incompatible with PyTecplot
    # and must be set to "spawn"
    multiprocessing.set_start_method('spawn')

    # Get the datafiles
    files = glob.glob('hotwatermixing/HotWaterMixing_Y05YT10*.plt')

    # Set up the pool with initializing function and associated arguments
    num_workers = min(multiprocessing.cpu_count(), len(files))
    pool = multiprocessing.Pool(num_workers, initializer=init)

    try:
        if not os.path.exists('images'):
            os.makedirs('images')

        # Map the work function to each of the job arguments
        results = pool.map(work, files)
    finally:
        # !!! IMPORTANT !!!
        # Must join the process pool before parent script exits
        # to ensure Tecplot cleans up all temporary files
        # and does not create a core dump
        pool.close()
        pool.join()

    Z, ZT, chisq_per_ndf, stddev_vy, stddev_t, y0 = zip(*results)

    from scipy import interpolate
    from matplotlib import pyplot

    x = np.linspace(min(Z), max(Z), 300)
    y = np.linspace(min(ZT), max(ZT), 300)
    XX, YY = np.meshgrid(x, y)

    fig, ax = pyplot.subplots(2, 2)
    for ax, data in zip(ax.ravel(), (chisq_per_ndf, stddev_vy, stddev_t, y0)):
        ZZ = interpolate.griddata((Z, ZT), data, (XX, YY))
        plt = ax.pcolormesh(XX, YY, ZZ)
        ax.scatter(Z, ZT)
        fig.colorbar(plt, ax=ax)
    pyplot.show()

