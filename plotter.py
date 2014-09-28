#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging

# Import modules for CGI handling 
import cgi, cgitb 
import plot

# Create instance of FieldStorage 

if __name__ == "__main__":
#	cgi.test()
	print "Content-type:text/html\r\n\r\n"

	cgitb.enable()
	form = cgi.FieldStorage()
	begin = form.getvalue('begin')
	end  = form.getvalue('end')
	print plot.draw_svg(None, None)
    
    	print begin, end
    
