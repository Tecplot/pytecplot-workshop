import glob
import os
import re
import sys

import tecplot as tp
from tecplot.constant import *


def frame_grid(nrows, ncols):
    scale = max(nrows, ncols)
    page = tp.add_page()
    frames = []
    for row in range(nrows):
        frame_row = []
        for col in range(ncols):
            frame = page.add_frame() if row or col else page.active_frame()
            pos = (scale * col / ncols, scale * (1 - row / nrows))
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

files = sorted(glob.glob('HotWaterMixing_Y05YT10*.plt'))
pattern = re.compile(r'HotWaterMixing_Y05YT10Z(\d+)ZT(\d+).plt')

filename = 'HotWaterMixing_Y05YT10Z{:0>2}ZT{:0>3}.plt'

Z, ZT = zip(*[[int(x) for x in pattern.match(f).groups()] for f in files])
Z = sorted(set(Z))
ZT = sorted(set(ZT))

frames = frame_grid(len(ZT), len(Z))
for zt, frame_row in zip(ZT, frames):
    for z, frame in zip(Z, frame_row):
        fname = filename.format(z, zt)
        if os.path.exists(fname):
            dataset = tp.data.load_tecplot(fname, frame=frame)
            frame.load_stylesheet('isosurface.sty')

tp.save_png('hotwater-grid-stylesheet.png')
