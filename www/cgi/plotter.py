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

  if getvals['end'] > lastvalue:
    getvals['end'] = lastvalue
  if getvals['begin'] < firstvalue:
    getvals['begin'] = firstvalue
    
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
  print "Content-type:text/html\r\n\r\n"
  print webreq(form)

