#!/usr/bin/env python
# encoding: utf-8

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
  tend =   int(time.time())
  tbegin = tend - 60*60*int(cfg.get('settings', 'default_view_hours'))

  timeformat = cfg.get('settings', 'timeformat')

  getvals = {
    'begin': time.strftime(timeformat, time.localtime(tbegin)),
    'end': time.strftime(timeformat, time.localtime(tend)),
    'width': 960,
    'height' : 720
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
    getvals['begin'] = tbegin

  if getvals['end'] > tend:
    getvals['end'] = tend

  firstvalue, lastvalue = plot.data_span(timeformat)
  if getvals['begin'] < firstvalue:
    getvals['begin'] = firstvalue

  # test that begin is before  begin
  if getvals['begin'] > getvals['end']:
    getvals['begin'] = tbegin
    getvals['end'] = tend

  return plot.draw_svg(getvals['begin'], getvals['end'], 
                      int(getvals['width']), int(getvals['height']))

if __name__ == "__main__":
  form = cgi.FieldStorage()
  print "Content-type:text/html\r\n\r\n"
  print webreq(form)
  
