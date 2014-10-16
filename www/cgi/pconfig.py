#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import os
import json
import cgi


def field_setup():
    return [
        { 'key': "node_name",
            'defval': "",
            'label' : "Node Name",
            "type" : "smalltxt",
            "range" : None ,
            "webconfigurable": True,
            "description": "Short name for the node"
        },
        { 'key': "node_netaddress",
            'defval': "localhost",
            'label' : "Node Network Address",
            "type" : "smalltxt",
            "range" : None,
            "webconfigurable": True,
            "description": "DNS or IP address through which to reach the node",
        },
        { 'key': "node_description",
            'defval': "USE THIS TO IDENTIFIY THE POSITION OF THE NODE",
            'label' : "Node Description",
            "type" : "largetxt",
            "range" : None,
            "webconfigurable": True,
            "description": """Longer description of the node, potentially usefull for locating the    node when it sends out an alarm.""",
        },
        { 'key': "temperature_max",
            'defval': 26,
            'label' : "Maximum Temperature",
            "type" : "intrange",
            "range" : [-273,100],
            "webconfigurable": True,
            "description": "Temperature upper treshhold in Celsisus for sending an e-mail alarm.",
        },
        { 'key': "humidity_min",
            'defval': 35,
            'label' : "Minimum Humidity",
            "type" : "intrange",
            "range" : [0,100],
            "webconfigurable": True,
            "description": "Humidty lower percentage treshhold  for sending an e-mail alarm.",
        },
        { 'key': "humidity_max",
            'defval': 65,
            'label' : "Maximum Humidity",
            "type" : "intrange",
            "range" : [0,100],
            "webconfigurable": True,
            "description": "Humidty upper percentage treshhold for sending an e-mail alarm.",
        },
        { 'key': "alarm_from_address",
            'defval': "root@localhost",
            'label' : "Alarm From Address",
            "type" : "email",
            "range" : None,
            "webconfigurable": True,
            "description": "Sender e-mail adresser for alarm mails.",
        },
        { 'key': "alarm_to_addresses",
            'defval': "root@localhost",
            'label' : "Alarm Recipients",
            "type" : "largetxt",
            "range" : None,
            "webconfigurable": True,
            "description": "List of ;-seperated addresses to send alarm e-mails to.",
        },
        { 'key': "SMTP_server",
            'defval': "smtp.gmail.com:587",
            'label' : "SMTP Mailserver",
            "type" : "smalltxt",
            "range" : None,
            "webconfigurable": True,
            "description": "URI for the SMTP server through which to send e-mail alarms.",
        },
        { 'key': "SMTP_username",
            'defval': "",
            'label' : "SMTP Username",
            "type" : "smalltxt",
            "range" : None,
            "webconfigurable": True,
            "description": "Optional, for use with  smtp servers requiring authentication ie. gmail",
        },
        { 'key': "SMTP_password",
            'defval': "",
            'label' : "SMTP Password",
            "type" : "password",
            "range" : None,
            "webconfigurable": True,
            "description": "Optional, for use with  smtp servers requiring authentication ie. gmail",
        },
        { 'key': "default_view_hours",
            'defval': 48,
            'label' : "Default Data View",
            "type" : "intrage",
            "range" : [1, 120],
            "webconfigurable": True,
            "description": "Number of hours prior for default dataview.",
        },

        { 'key': "tmp_dir",
            'defval': "/ramdisk",
            'label' : "tmp storage for working data",
            "type" : "smalltxt",
            "range" : None,
            "webconfigurable": False,
            "description": "You can change this in the cfg file, but you should leave it to a qualified programmer.",
        },
        { 'key': "data_dir",
            'defval': "data",
            'label' : "permanent storage location relative to cgi dir",
            "type" : "smalltxt",
            "range" : None,
            "webconfigurable": False,
            "description": "You can change this in the cfg file, but you should leave it to a qualified programmer.",
        },
        { 'key': "max_plot_points",
            'defval': 640,
            'label' : "Wobbly limit on number of points in plots.",
            "type" : "intrange",
            "range" : [10, 4096],
            "webconfigurable": False,
            "description": """You can change this in the cfg file, but you should leave it to a qualified programmer.""",
        },
        { 'key': "sample_period",
            'defval': 10,
            'label' : "Minutes between data points, also number of samples that a datapoint is averaged from",
            "type" : "intrange",
            "range" : [1, 120],
            "webconfigurable": False,
            "description": """You can change this in the cfg file, but you should leave it to a qualified programmer.""",
        },
    ]

def json_out():        
    cfg = read("rb_preserve.cfg")
    elist = field_setup()
    outup = {}
    for i in range(len(elist)):
        if not elist[i]['webconfigurable']:
            continue
        de = elist[i]
        de["value"] = cfg.get('settings', de['key'])
        outup[i] = de
    return outup

def read(fname):
    dflts = {}

    for de in field_setup():
        dflts[de["key"]] = de["defval"]

    #read config file if present
    cfg = ConfigParser.RawConfigParser(dflts)
    if os.path.exists(fname):
        cfg.read(fname)

    if not cfg.has_section("settings"):
        cfg.add_section('settings')

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
        cfg.set('settings', k, form[k])
    write(cfg, 'rb_preserve.cfg')
    
    return "Content-type:text/html\r\n\r\n%s" % json.dumps(json_out())
    
if __name__ == "__main__":
    form = cgi.FieldStorage()
    print webreq(form)

