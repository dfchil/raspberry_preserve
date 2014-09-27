#!/usr/bin/env python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 

if __name__ == "__main__":
    form = cgi.FieldStorage() 
    begin = form.getvalue('begin')
    end  = form.getvalue('end')
    
    print begin, end