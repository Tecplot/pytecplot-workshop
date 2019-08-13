import glob
import os
import re
import sys

import tecplot as tp
from tecplot.constant import *

def frame_grid(nrows, ncols):
    scale = max(nrows, ncols)
    frames = []
    for row in range(nrows):
        frame_row = []
        for col in range(ncols):
            if row or col:
                frame = tp.active_page().add_frame()
            else:
                frame = tp.active_page().active_frame()
            pos = (scale * col / ncols,
                   scale * (1 - row / nrows))
            height = scale / nrows
            width = scale / ncols
            frame.position = pos
            frame.height = height
            frame.width = width
            frame_row.append(frame)
        frames.append(frame_row)
    tp.macro.execute_command('$!WorkspaceView FitAllFrames')
    return frames

if '-c' in sys.argv:
    tp.session.connect(port=7601)
    tp.new_layout()

# get list of input data files
files = sorted(glob.glob('hotwatermixing/HotWaterMixing_Y05YT10*.plt'))

# setup regular expression to extract input velocity (Z) and temperature (ZT)
pattern = re.compile(r'Z(\d+)ZT(\d+)')

# filename format
filename = 'hotwatermixing/HotWaterMixing_Y05YT10Z{:0>2}ZT{:0>3}.plt'

# get sorted values of input velocity (Z) and temperature (ZT)
Z, ZT = zip(*[[int(x)
               for x in pattern.search(f).groups()]
              for f in files])
Z = sorted(set(Z))
ZT = sorted(set(ZT))

# create grid of frames
frames = frame_grid(len(ZT), len(Z))

# in each frame, load data and adjust plot style using stylesheet
for zt, frame_row in zip(ZT, frames):
    for z, frame in zip(Z, frame_row):
        datafile = filename.format(z, zt)
        if os.path.exists(datafile):
            tp.data.load_tecplot(datafile, frame=frame)
            frame.load_stylesheet('isosurface.sty')

tp.save_png('hotwater-grid-stylesheet.png')

