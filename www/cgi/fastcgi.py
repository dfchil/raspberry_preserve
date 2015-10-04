#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

import cgi
from flup.server.fcgi import WSGIServer

import plotter
import serverside_js
import pconfig
import mail

def app(env, start_response):
    if (env['REQUEST_URI']).startswith("/cgi/plotter.py"):
      start_response('200 OK', [('Content-Type', "image/svg+xml")])
      form = cgi.FieldStorage(environ=env)
      yield plotter.webreq(form)

    elif env['REQUEST_URI'] == "/cgi/serverside_js.py":
      start_response('200 OK', [('Content-Type', 'application/javascript')])
      yield serverside_js.webreq()

    elif (env['REQUEST_URI']).startswith("/cgi/pconfig.py"):
      start_response('200 OK', [('Content-Type', 'application/json')])
      form = cgi.FieldStorage(environ=env)
      yield pconfig.webreq(form)

    elif (env['REQUEST_URI']).startswith("/cgi/mail.py"):
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
