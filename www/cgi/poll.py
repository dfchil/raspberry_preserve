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
import mail

def poll():
    sensor = Adafruit_DHT.AM2302
    pin = 4
    return Adafruit_DHT.read_retry(sensor, pin)

def warning_test(humidity, temperature, cfg):
    #if humidity outside range
    if humidity < float(cfg.get('settings', 'humidity_min')):
        mail.send_warning("Low humidty", humidity, cfg)
    if humidity > float(cfg.get('settings', 'humidity_max')):
        mail.send_warning("High humidty", humidity, cfg)

    if temperature > float(cfg.get('settings', 'temperature_max')):
        mail.send_warning("High temperature", temperature, cfg)

def condense(tmplnes):
    td = []
    for lt in tmplnes:
        try:
            h, t = lt.split(',')
            h = float(h)
            t = float(t)
            td.append((h,t))
        except:
            continue
    tmplnes = []
    th = 0.0;
    tt = 0.0;
    for i in range(len(td)):
        th += td[i][0]
        tt += td[i][1]

    th /= len(td)
    tt /= len(td)
    return (th, tt)

def main(argv=None):
    cfg = pconfig.read('rb_preserve.cfg')

    ddir = cfg.get('settings', 'data_dir')
    timeformat = pconfig.dformat();
    pwd = os.path.dirname(os.path.realpath(__file__))

    #sample sensor
    humidity = None
    temperature = None

    while humidity == None and temperature == None:
        humidity, temperature = poll()

    # see if
    tmpfn = os.path.join(cfg.get('settings', 'tmp_dir'), "intermediary.data")

    if os.path.exists(tmpfn):
        with open(tmpfn, 'r') as pd:
            lines = pd.readlines()
    else:
        lines = []

    lines.append("%.2f,%.02f\n" % (humidity, temperature))

    if len(lines) >= int(cfg.get('settings', 'sample_period')):
        avg_hum, avg_temp = condense(lines)
        warning_test(avg_hum, avg_temp, cfg)
        lines = []   # zerro tmp file

        #store in persistent file
        pfname = "%s/%s/%s.data" % (pwd, ddir, time.strftime(pconfig.dfilename_fmt()))
        pstr = "%s,%.2f,%.02f\n" % (time.strftime(timeformat), avg_hum, avg_temp)
        with open(pfname, "a") as outfile:
            outfile.write(pstr)

    #overwrite existing tmp file with current data
    with open(tmpfn, 'w') as pd:
        pd.write("".join(lines))

if __name__ == "__main__":
    import Adafruit_DHT
    sys.exit(main())
