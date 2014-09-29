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
from subprocess import call
import time

def filerange(begin, end):
    return ["2014-09.data"]
    
def data_stride(begin, end, num_points):
    stride = ((end - begin) / 60)/num_points
    stride = 1 if stride < 1 else stride
    return int(stride)

def _l2secs(line):
    tl = line.split(',')[0]
    return time.mktime(time.strptime(tl, pconfig.dformat()))

def get_lines(begin, end):
    lines = []
    stride = data_stride(begin, end, 640)
    for fn in filerange(begin, end):
        with  open("data/%s"% fn, 'r') as f:
            for l in f.readlines()[0::stride]:
                try:
                    ts = _l2secs(l)
                    if ts > begin and ts < end:
                        lines.append(l)
                except:
                    continue
                
    return lines

def write_gpcfg():
    pass


def draw_svg(begin, end, width, height):
    
    uid = str(uuid.uuid4())

    #write data file
    with open("/ramdisk/%s.data" % uid, "w") as dfo:
        dfo.write("".join(get_lines(begin, end)))
    
    #write gnuplot cfg file
    gpcfg = """
    set terminal svg size %d,%d dashed linewidth 0.7
    set output '/ramdisk/%s.svg'
    
    set bmargin 6.0
    set key right top

    set yrange [30:75.5]
    set y2range [*:27]

    set datafile separator ","

    set timefmt '%s'
    set xdata time

    set ytics 5 nomirror tc rgb "blue"
    set ylabel 'Humidity' tc rgb "blue"

    set y2tics 1 nomirror tc rgb "red"
    set y2label 'Temperature'  tc rgb "red"

    plot '/ramdisk/%s.data' \
        using 1:2 with lines lt 1 linecolor rgb "blue" title 'Humidity %%', \
    ''  using 1:3 with lines lt 1 linecolor rgb "red" title 'Degrees Celsius' axes x1y2 , \
    	35  with lines lt 3 linecolor rgb "blue" title "Humidity limits", \
    	65  with lines lt 3 linecolor rgb "blue" title "", \
    	26  with lines lt 3 linecolor rgb "red" title "Temperature max" axes x1y2
        
    """ % (width, height, uid, pconfig.dformat(), uid)
    
    gpcfgfn  = "/ramdisk/%s.gp" % uid
    with open(gpcfgfn, "w") as gpfo:
        gpfo.write(gpcfg)
    
    call(["gnuplot", "%s" %gpcfgfn])

    with  open("/ramdisk/%s.svg" % uid, 'r') as f:
        outp = f.read()
    call(["rm", "/ramdisk/%s.gp" % uid, "/ramdisk/%s.data" % uid, "/ramdisk/%s.svg" % uid])

    return outp

# if __name__ == "__main__":
#     print draw_svg(None, None)
