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

# Import modules for CGI handling
import cgi, cgitb
import plot
import pconfig
import time

def cond_read(strnme, alt, form):
    outp = form.getvalue(strnme)
    return outp if outp != None else alt

def webreq(form):
  cfg = pconfig.read('rb_preserve.cfg')

  #default time is past 24 hours
  firstvalue, lastvalue = plot.data_span()

  tend =   lastvalue
  deftimeview = 60*60*int(cfg.get('settings', 'default_view_hours'))

  timeformat = pconfig.dformat()

  getvals = {
    'begin': time.strftime(timeformat, time.localtime(tend - deftimeview)),
    'end': time.strftime(timeformat, time.localtime(tend)),
    'width': 960,
    'height' : 720,
    'origin' : ""
  }

  for k,v in getvals.iteritems():
    getvals[k] = cond_read(k, v, form)

  #try parsing string values
  try:
    getvals['end'] = time.mktime(time.strptime(getvals['end'], timeformat))
  except:
    getvals['end'] = tend

  try:
    getvals['begin'] = time.mktime(time.strptime(getvals['begin'], timeformat))
  except:
    getvals['begin'] = tend - deftimeview


  # test that begin is before end
  if getvals['begin'] >= getvals['end']:
      if getvals['origin'] == "end":
        getvals['begin'] = getvals['end'] - deftimeview
      elif getvals['end'] >= tend:
        getvals['begin'] = tend - deftimeview
        getvals['end'] = tend
      else:
        getvals['end'] = getvals['begin'] + deftimeview

  if getvals['end'] >= tend:
    getvals['end'] = tend
  elif getvals['end'] <= firstvalue:
    getvals['end'] = firstvalue + deftimeview
    getvals['begin'] = firstvalue

  if getvals['begin'] < firstvalue:
    getvals['begin'] = firstvalue

  return plot.draw_svg(getvals['begin'], getvals['end'],
                      int(getvals['width']), int(getvals['height'])).replace("</svg>","""
  <script type="text/javascript">
    top.max_secs = function(){return %f;};
    top.show_range();
    top.set_time_pickers(%f, %f);
  </script>
</svg>""" % (lastvalue *1000, getvals['begin']*1000, getvals['end']*1000))
#

if __name__ == "__main__":
  form = cgi.FieldStorage()
  print "Content-type:text/html\r\n\r\n %s" % webreq(form)

