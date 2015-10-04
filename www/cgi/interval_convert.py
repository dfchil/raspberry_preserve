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

import sys
import time
import os
import pconfig


def _parse_date(datestr, tformat):
    return time.strptime(datestr, tformat)

def get_lines(tformat, cond_fac):
    lines = []
    tmplnes = []
    for fn in ["2014-09.data.old"]:
        with  open("data/%s"% fn, 'r') as f:
            for l in f.readlines():
                tmplnes.append(l)

                if len(tmplnes) == cond_fac:
                    td = []
                    date = None
                    for lt in tmplnes:
                        try:
                            d, h, t = lt.split(',')
                            h = float(h)
                            t = float(t)
                            date = _parse_date(d, tformat)
                            td.append((h,t))
                        except:
                            continue
                    tmplnes = []
                    if date != None:
                        th = 0.0;
                        tt = 0.0;
                        for i in range(len(td)):
                            th += td[i][0]
                            tt += td[i][1]

                        date = time.strftime(cfg.get('settings', 'timeformat'), date)
                        th /= len(td)
                        tt /= len(td)
                        lines.append("%s,%.2f,%.02f\n" % (date, th, tt))
    return lines

if __name__ == "__main__":
    cfg = pconfig.read('rb_preserve.cfg')
    # print "".join(get_lines(cfg.get('settings', 'timeformat'), 10))

    with  open("data/2014-09.data", 'r') as f:
        lines = f.readlines()

    endtime = time.time() #+ time.timezone
    begintime = endtime - len(lines)*600

    outlines = []

    for l in lines:
        _, h, t = l.split(',')
        ttime = time.localtime(begintime)
        ttime = time.strftime(cfg.get('settings', 'timeformat'), ttime)
        begintime += 600
        outlines.append("%s,%s,%s" % (ttime, h, t))

    print "".join(outlines)
