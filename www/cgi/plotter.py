#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging

# Import modules for CGI handling 
import cgi, cgitb 
import plot
import pconfig
import time

# Create instance of FieldStorage 


print "Content-type:text/html\r\n\r\n"

# cgitb.enable()
form = cgi.FieldStorage()
begin = form.getvalue('begin')
end  = form.getvalue('end')

if end == None:
    end = time.strftime(pconfig.dformat())

if begin == None:
    begin = time.strftime(pconfig.dformat(), time.localtime(int(time.time() - 60*60*24)))

end = time.mktime(time.strptime(end, pconfig.dformat()))
begin =  time.mktime(time.strptime(begin, pconfig.dformat()))

print plot.draw_svg(begin, end)
