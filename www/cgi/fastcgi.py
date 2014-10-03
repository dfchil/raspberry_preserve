#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
from urlparse import urlparse, parse_qs

import sys, os
from flup.server.fcgi import WSGIServer

import plotter
import serv_js

def app(env, start_response):
    if env['SCRIPT_NAME'] == "/cgi/plotter.py":
      start_response('200 OK', [('Content-Type', "image/svg+xml")])
      form = cgi.FieldStorage(environ=env)
      yield plotter.webreq(form)

    elif env['SCRIPT_NAME'] == "/cgi/serverside.js.py":
      start_response('200 OK', [('Content-Type', 'application/javascript')])
      yield serv_js.webreq()

    else:
      start_response('200 OK', [('Content-Type', 'text/html')])
      yield '<h1>FastCGI Environment</h1>'
      yield '<table>'
      for k, v in sorted(env.items()):
           yield '<tr><th>%s</th><td>%s</td></tr>' % (k, v)
      yield '</table>'
      

if __name__ == "__main__":
    WSGIServer(app).run()
