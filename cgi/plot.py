#!/usr/bin/env python
# encoding: utf-8

# get range
# calculate list of files spanned by range
# calculate sample stride from range
# read samples from files
# output to /tmp/uuid.dt file 
# write /tmp/uuid.gp file
# use gnuplot to generate /tmp/uuid.svg
# serve contents of /tmp/uuid.svg

import sys
import pconfig
import uuid
from subprocess import call

def filerange(begin, end):
    return ["2014-09.data"]
    
def data_stride(begin, end):
    return 1

def get_lines(begin, end):
    lines = []
    stride = data_stride(begin, end)
    for fn in filerange(begin, end):
        with  open("data/%s"% fn, 'r') as f:
            lines.extend(f.readlines()[0::stride])

    return lines

def write_gpcfg():
    pass


def draw_svg(begin, end):
    
    uid = str(uuid.uuid4())

    #write data file
    with open("/tmp/%s.data" % uid, "w") as dfo:
        dfo.write("".join(get_lines(begin, end)))
    
    
    height = 720
    width = 1280
    
    #write gnuplot cfg file
    gpcfg = """
    set terminal svg size %d,%d solid linewidth 0.7
    set output '/tmp/%s.svg'

    # set lmargin 7.5
    # set bmargin 6.0
    # set rmargin 7.0
    # set tmargin 1.4

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

    plot '/tmp/%s.data' \
        using 1:2 with lines linecolor rgb "blue" title 'Humidity', \
    ''  using 1:3 with lines linecolor rgb "red" title 'Temperature' axes x1y2 , \
    	35  with lines lt 0 linecolor rgb "blue" title "Humidity limits", \
    	65  with lines lt 0 linecolor rgb "blue" title "", \
    	26  with lines lt 0 linecolor rgb "red" title "Temperature max" axes x1y2
        
    """ % (width, height, uid, pconfig.dformat(), uid)
    
    gpcfgfn  = "/tmp/%s.gp" % uid
    with open(gpcfgfn, "w") as gpfo:
        gpfo.write(gpcfg)
    
    call(["gnuplot", "%s" %gpcfgfn])
    
    with  open("/tmp/%s.svg" % uid, 'r') as f:
        return f.read()

# if __name__ == "__main__":
#     print draw_svg(None, None)