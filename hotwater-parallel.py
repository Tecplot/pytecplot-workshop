import atexit
import glob
import os
import multiprocessing
import sys

import tecplot as tp

def init():
    # !!! IMPORTANT !!!
    # Must register stop at exit to ensure Tecplot cleans
    # up all temporary files and does not create a core dump
    atexit.register(tp.session.stop)

def work(datafile):
    tp.new_layout()
    tp.data.load_tecplot(datafile)
    tp.active_frame().load_stylesheet('isosurface.sty')
    imgfile = os.path.basename(datafile).replace('.plt', '.png')
    tp.save_png(os.path.join('images', imgfile))

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
        pool.map(work, files)
    finally:
        # !!! IMPORTANT !!!
        # Must join the process pool before parent script exits
        # to ensure Tecplot cleans up all temporary files
        # and does not create a core dump
        pool.close()
        pool.join()

