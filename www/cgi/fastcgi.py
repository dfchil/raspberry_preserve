#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
from urlparse import urlparse, parse_qs

import sys, os
from flup.server.fcgi import WSGIServer

import plotter
import serverside_js
import pconfig
import mail

def app(env, start_response):
    if env['SCRIPT_NAME'] == "/cgi/plotter.py":
      start_response('200 OK', [('Content-Type', "image/svg+xml")])
      form = cgi.FieldStorage(environ=env)
      yield plotter.webreq(form)

    elif env['SCRIPT_NAME'] == "/cgi/serverside_js.py":
      start_response('200 OK', [('Content-Type', 'application/javascript')])
      yield serverside_js.webreq()

    elif env['SCRIPT_NAME'] == "/cgi/pconfig.py":
      start_response('200 OK', [('Content-Type', 'application/json')])
      form = cgi.FieldStorage(environ=env)
      yield pconfig.webreq(form)

    elif env['SCRIPT_NAME'] == "/cgi/mail.py":
      start_response('200 OK', [('Content-Type', 'text/html')])
      form = cgi.FieldStorage(environ=env)
      yield mail.webreq(form)


    else:
      start_response('200 OK', [('Content-Type', 'text/html')])
      yield '<h1>FastCGI Environment</h1>'
      yield '<table>'
      for k, v in sorted(env.items()):
           yield '<tr><th>%s</th><td>%s</td></tr>' % (k, v)
      yield '</table>'
      

if __name__ == "__main__":
    WSGIServer(app).run()
