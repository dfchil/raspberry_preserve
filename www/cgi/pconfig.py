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

import ConfigParser
import os
import json
import cgi
import stat

def field_setup():
    return [
        {   'key': "node_name",
            'defval': "",
            'label' : "Node Name",
            "type" : "smalltxt",
            "range" : None ,
            "webconfigurable": True,
            "description": """Short name for the node"""
        },
        {   'key': "node_netaddress",
            'defval': "localhost",
            'label' : "Node Network Address",
            "type" : "smalltxt",
            "webconfigurable": True,
            "description": """DNS or IP address through which to reach the node""",
        },
        {   'key': "node_description",
            'defval': "USE THIS TO IDENTIFIY THE POSITION OF THE NODE",
            'label' : "Node Description",
            "type" : "largetxt",
            "webconfigurable": True,
            "description": """Longer description of the node, potentially usefull
for locating the node when it sends out an alarm.""",
        },
        {   'key': "alarm_from_address",
            'defval': "root@localhost",
            'label' : "Alarm From Address",
            "type" : "email",
            "webconfigurable": True,
            "description": """Sender e-mail adresser for alarm mails.""",
        },
        {   'key': "alarm_to_addresses",
            'defval': "root@localhost",
            'label' : "Alarm Recipients",
            "type" : "largetxt",
            "webconfigurable": True,
            "description": """List of ;-seperated addresses to send alarm
e-mails to.""",
        },
        {   'key': "SMTP_server",
            'defval': "smtp.gmail.com:587",
            'label' : "SMTP Mailserver",
            "type" : "smalltxt",
            "webconfigurable": True,
            "description": """URI for the SMTP server through which to send
e-mail alarms.""",
        },
        {   'key': "SMTP_username",
            'defval': "",
            'label' : "SMTP Username",
            "type" : "smalltxt",
            "webconfigurable": True,
            "description": """Optional, for use with  smtp servers requiring
authentication ie. gmail""",
        },
        {   'key': "SMTP_password",
            'defval': "",
            'label' : "SMTP Password",
            "type" : "password",
            "webconfigurable": True,
            "description": """Optional, for use with  smtp servers requiring
authentication ie. gmail""",
        },
        {   'key': "sample_period",
            'defval': 10,
            'symbol': " minutes",
            'label' : "Recording Interval",
            "type" : "intrange",
            "range" : [1, 120],
            "webconfigurable": True,
            "description": """Interval in minutes between data point recording,
also number of samples that a datapoint is averaged from.

The system is capabale of handling mixed histories of varying sampling intervals.
""",
        },
        {   'key': "temperature_max",
            'defval': 26,
            'symbol': ' ℃',
            'label' : "Maximum Temperature",
            "type" : "intrange",
            "range" : [-273,100],
            "webconfigurable": True,
            "description": """Temperature upper treshhold in degrees Celsius for sending
an e-mail alarm.""",
        },
        {   'key': "humidity_min",
            'defval': 35,
            'symbol': " %",
            'label' : "Minimum Humidity",
            "type" : "intrange",
            "range" : [0,100],
            "webconfigurable": True,
            "description": """Humidty lower percentage treshhold  for sending an
e-mail alarm.""",
        },
        {   'key': "humidity_max",
            'defval': 65,
            'symbol': " %",
            'label' : "Maximum Humidity",
            "type" : "intrange",
            "range" : [0,100],
            "webconfigurable": True,
            "description": """Humidty upper percentage treshhold for sending an
e-mail alarm.""",
        },
        {   'key': "default_view_hours",
            'defval': 48,
            'symbol': " hours",
            'label' : "Default Data View",
            "type" : "intrange",
            "range" : [1, 720],
            "webconfigurable": True,
            "description": """Number of hours prior for default dataview.""",
        },

        {   'key': "tmp_dir",
            'defval': "/run/shm",
            'label' : "tmp storage for working data",
            "type" : "smalltxt",
            "webconfigurable": False,
            "description": """"You can change this in the cfg file, but you
should leave it to a qualified programmer.""",
        },
        {   'key': "data_dir",
            'defval': "data",
            'label' : "permanent storage location relative to cgi dir",
            "type" : "smalltxt",
            "webconfigurable": False,
            "description": """"You can change this in the cfg file, but you
should leave it to a qualified programmer.""",
        },
        {   'key': "max_plot_points",
            'defval': 320,
            'symbol': " sample points",
            'label' : "Plot Resolution",
            "type" : "logrange",
            "range" : [32, 4096],
            "webconfigurable": True,
            "description": """Soft limit on number of sample points in plots.""",
        },
    ]

def json_out():
    cfg = read("rb_preserve.cfg")
    elist = field_setup()
    outup = {}
    i = 0
    for de in elist:
        if not de['webconfigurable']:
            continue
        de["value"] = cfg.get('settings', de['key'])
        outup[i] = de
        i+=1
    return json.dumps(outup, sort_keys=False,indent=2, separators=(',', ': '))

def read(fname):

    #read config file if present
    cfg = ConfigParser.ConfigParser(allow_no_value=True)
    if os.path.exists(fname):
        cfg.read(fname)

    if not cfg.has_section("settings"):
        cfg.add_section('settings')

    for de in field_setup():
        if not cfg.has_option('settings', de["key"]):
            cfg.set('settings', de["key"], str(de["defval"]))

    return cfg

def write(cfg, fname):
    with open(fname, 'w') as cfgfile:
        cfg.write(cfgfile)

def dformat():
    return "%Y-%m-%d %H:%M"

def dfilename_fmt():
    return "%Y-%m"

def webreq(form):
    cfg = read('rb_preserve.cfg')
    for k in form.keys():
        cfg.set('settings', k, form[k].value)
    write(cfg, 'rb_preserve.cfg')

    return  json_out()

if __name__ == "__main__":
    form = cgi.FieldStorage()
    print "Content-type:application/json\r\n\r\n%s" % webreq(form)

