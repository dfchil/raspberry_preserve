#!/usr/bin/env python
# encoding: utf-8

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

def data_span(tformat):
    dfiles = sorted(glob.glob("./data/*.data"))
    
    first = time.time()
    last = first

    if len(dfiles):
        with open(dfiles[0]) as ffile:
            first = _l2secs(ffile.readline(), tformat)
            
        last = _l2secs(check_output(["tail", "-n", "1", dfiles[-1]]), tformat)
    return (first, last)

def filerange(begin, end):
    return ["2014-09.data", "2014-10.data"]

def data_stride(begin, end, max_points, sample_interval):
    stride = math.floor(((end - begin) / sample_interval)/max_points)
    stride = 1 if stride < 1 else stride
    return int(stride)

def _l2secs(line, tformat):
    tl = line.split(',')[0]
    return time.mktime(time.strptime(tl, tformat))

def get_lines(begin, end, tformat, max_points, sample_interval):
    lines = []
    stride = data_stride(begin, end, max_points, sample_interval)
    for fn in filerange(begin, end):
        with open("data/%s"% fn, 'r') as f:
            flines = f.readlines()
        if len(flines)> 0:
            # begin_off  = _l2secs(flines[0], tformat)
            # begin_off = int(( begin- begin_off) / sample_interval)
            # begin_off = begin_off if begin_off > 0 else 0
            # end_off  = _l2secs(flines[-1], tformat)
            # end_off = int((end_off - end) / sample_interval)
            # end_off = -end_off if end_off > 0 else len(flines)
            # lines.extend(flines[begin_off:end_off:stride])
            for l in flines[::stride]:
                try:
                    ts = _l2secs(l, tformat)
                    if ts > begin and ts < end:
                        lines.append(l)
                except:
                    continue
    # print len(lines), stride, begin_off, end_off
    return lines


def write_gpcfg(width, height, uid_fbase, cfg):
    
    timeformat = cfg.get('settings', 'timeformat')
    hmin = float(cfg.get('settings', 'humidity_min'))
    hmax = float(cfg.get('settings', 'humidity_max'))
    tmax = float(cfg.get('settings', 'temperature_max'))
    
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

    plot '%s.data' \
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
    with open("%s.data" % uid_fbase, "w") as dfo:
        dfo.write("".join(get_lines(begin, end, 
                          cfg.get('settings', 'timeformat'), 
                          int(cfg.get('settings', 'max_plot_points')),
                          int(cfg.get('settings', 'sample_period'))*60)))
    #write gnuplot cfg file
    write_gpcfg(width, height, uid_fbase, cfg)
    
    # make gnuplot generate the svg file
    outp = check_output(["gnuplot", "%s.gp" % uid_fbase ])

    #clean up tmp files
    os.remove("%s.gp" % uid_fbase)
    os.remove("%s.data" % uid_fbase)

    return outp
