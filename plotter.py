#!/usr/bin/env python

# Import modules for CGI handling 
import cgi, cgitb 
import plot

# Create instance of FieldStorage 

if __name__ == "__main__":
    # form = cgi.FieldStorage()
    # begin = form.getvalue('begin')
    # end  = form.getvalue('end')

    print plot.draw_svg(None, None)
    #
    # print begin, end
    
