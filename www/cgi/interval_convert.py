#!/usr/bin/env python
# encoding: utf-8

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
    print "".join(get_lines(cfg.get('settings', 'timeformat'), 10))
