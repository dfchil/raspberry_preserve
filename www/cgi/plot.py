#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2014 Daniel Fairchild
#
# This file is part of raspberry_preserve.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

# get range
# calculate list of files spanned by range
# calculate sample stride from range
# read samples from files
# output to /ramdisk/uuid.dt file
# write /ramdisk/uuid.gp file
# use gnuplot to generate /ramdisk/uuid.svg
# serve contents of /ramdisk/uuid.svg

import sys
import pconfig
import uuid
from subprocess import check_output
import time
import glob
import math
import os

from calendar import monthrange
from datetime import datetime, timedelta

from bisect import bisect_left, bisect_right


def _l2secs(line):
    tl = line.split(',')[0]
    return time.mktime(time.strptime(tl, pconfig.dformat()))

def data_span():
    dfiles = sorted(glob.glob("./data/*.data"))

    first = time.time()
    last = first

    if len(dfiles):
        with open(dfiles[0]) as ffile:
            first = _l2secs(ffile.readline())

        last = _l2secs(check_output(["tail", "-n", "1", dfiles[-1]]))
    return (first, last)

def filerange(begin, end):
  ltb =  datetime.fromtimestamp(begin)
  ltb =datetime(ltb.year, ltb.month, 1, 0, 0)
  lte =  datetime.fromtimestamp(end)
  output = []

  while ltb < lte:
    output.append("%s.data" % ltb.strftime(pconfig.dfilename_fmt()))
    mdays = monthrange(ltb.year, ltb.month)[1]
    ltb += timedelta(days=mdays)

  return output

def data_stride(begin, end, max_points, sample_interval):
    stride = math.floor(((end - begin) / sample_interval)/max_points)
    stride = 1 if stride < 1 else stride
    return int(stride)

def binary_search(bfun,  seekval, lines, low = 0, high=None):
    seekval = "%s,%.2f,%.02f\n" % (time.strftime(pconfig.dformat(), time.localtime(seekval)), 0.0, 0.0)
    high = high if high is not None else len(lines)

    pos = bfun(lines, seekval, low, high)
    pos = (pos if pos != high else high -1)

    return pos

def get_lines(begin, end, max_points, sample_interval):
    lines = []
    # stride = data_stride(begin, end, max_points, sample_interval)

    fr = filerange(begin, end)
    for i in range(len(fr)):
        with open("data/%s"% fr[i], 'r') as f:
            flines = f.readlines()
        if len(flines)> 0:
            boff = 0
            toff = len(flines) -1

        if i == 0:
            boff = binary_search(bisect_left, begin, flines)

        if i+1 == len(fr):
            toff = binary_search(bisect_right, end, flines)

        lines.extend(flines[boff:toff])

    stride = len(lines)/max_points
    stride = 1 if stride < 1 else int(stride)

    # print stride, max_points, len(lines)

    return lines[::stride]

def write_gpcfg(width, height, uid_fbase, cfg):

    timeformat =  pconfig.dformat()
    hmin = float(cfg.get('settings', 'humidity_min'))
    hmax = float(cfg.get('settings', 'humidity_max'))
    tmax = float(cfg.get('settings', 'temperature_max'))

    #set format x "%%d/%%m\n%%H:%%M"
    gpcfg = """
    set terminal svg size %d,%d dashed linewidth 0.7
    #set output '%s.svg'

    set bmargin 4.0
    set key right top

    set yrange [%f:%f]
    set y2range [*:%f]

    set datafile separator ","

    set timefmt '%s'
    set xdata time

    set ytics 5 nomirror tc rgb "blue"
    set ylabel 'Humidity' tc rgb "blue"

    set y2tics 1 nomirror tc rgb "red"
    set y2label 'Temperature'  tc rgb "red"

    plot '%s.tdata' \
        using 1:2 with lines lt 1 linecolor rgb "blue" title 'Humidity %%', \
    ''  using 1:3 with lines lt 1 linecolor rgb "red" title 'Degrees Celsius' axes x1y2 , \
    	%f  with lines lt 3 linecolor rgb "blue" title "Humidity limits", \
    	%f  with lines lt 3 linecolor rgb "blue" title "", \
    	%f  with lines lt 3 linecolor rgb "red" title "Temperature max" axes x1y2
    """ % ( width, height, uid_fbase,
            hmin-10, hmax+10, tmax+1.5,
            timeformat, uid_fbase, hmin, hmax, tmax)

    gpcfgfn  = "%s.gp" % uid_fbase
    with open(gpcfgfn, "w") as gpfo:
        gpfo.write(gpcfg)

def draw_svg(begin, end, width, height):

    cfg = pconfig.read('rb_preserve.cfg')

    uid_fbase =  "%s/%s" % (cfg.get('settings', 'tmp_dir') ,str(uuid.uuid4()))

    #write data file
    with open("%s.tdata" % uid_fbase, "w") as dfo:
        dfo.write("".join(get_lines(begin, end,
                        int(cfg.get('settings', 'max_plot_points')),
                        int(cfg.get('settings', 'sample_period'))*60)))
    #write gnuplot cfg file
    write_gpcfg(width, height, uid_fbase, cfg)

    # make gnuplot generate the svg file
    outp = check_output(["gnuplot", "%s.gp" % uid_fbase ])

    #clean up tmp files
    os.remove("%s.gp" % uid_fbase)
    os.remove("%s.tdata" % uid_fbase)

    return outp
