import atexit
import glob
import os
import multiprocessing
import re

import numpy as np
from scipy import interpolate, optimize, stats

import tecplot as tp
from tecplot.constant import *

def init():
    # !!! IMPORTANT !!!
    # Must register stop at exit to ensure Tecplot cleans
    # up all temporary files and does not create a core dump
    atexit.register(tp.session.stop)

def work(datafile):
    # file name includes input hot water velocity and temperature
    match = re.search(r'Z(\d+)ZT(\d+)', datafile)
    Z, ZT = int(match.group(1)), int(match.group(2))

    # load data and create a slice downstream of the tee of the pipe
    tp.new_layout()
    tp.data.load_tecplot(datafile)
    pipe_exit = tp.data.extract.extract_slice((0, 0.2, 0), (0, 1, 0))

    # get temperature on this slice
    t = pipe_exit.values('Temperature')[:]

    # return input velocity, intput temperature
    # and the stddev of the output temperature
    return Z, ZT, np.std(t)

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

    # unpack results
    v_in, t_in, std_t_out = zip(*results)

    # create a grid onto which we will interpolate the results
    vv, tt = np.meshgrid(v_in, t_in)
    std_t_out_interp = interpolate.griddata((v_in, t_in), std_t_out, (vv, tt))
    
    # create a new frame and dataset to hold the interpolated data in Tecplot
    frame = tp.active_page().add_frame()
    dataset = frame.create_dataset('Data', ['Input Velocity',
                                            'Input Temperature',
                                            'stddev(Output Temperature)'])
    zone = dataset.add_ordered_zone('Zone', std_t_out_interp.shape[::-1])

    # push the actual data into Tecplot
    zone.values('Input Velocity')[:] = vv
    zone.values('Input Temperature')[:] = tt
    zone.values('stddev(Output Temperature)')[:] = std_t_out_interp

    # plot results
    plot = frame.plot(PlotType.Cartesian2D)
    plot.activate()
    plot.show_contour = True

    plot.axes.axis_mode = AxisMode.Independent
    plot.view.fit_data()

    plot.contour(0).levels.reset_to_nice(20)
    plot.contour(0).legend.auto_resize = True

    tp.save_png('hotwater_std_t.png')

