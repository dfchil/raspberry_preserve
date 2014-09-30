#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging


import ConfigParser
import os


def read(fname):
    
    #default settings:
    dflts = {
        "node_name": "PLEASE SET MY NAME",
        "node_description": "USE THIS TO IDENTIFIY THE POSITION OF THE NODE",
        "node_netaddress": "rbp.ndrx.net",       #IP or DNS name
        "timeformat": "%Y-%m-%d %H:%M",         #don't change this
        "tmp_dir": "/ramdisk",
        "max_plot_points": 640,
        'data_dir': "data",
        'sample_period': 10,                   # minutes between stored samples 
        'temperature_max': 26,
        'humidity_min': 35,
        'humidity_max': 65,
        'alarm_to_addresses': "root@localhost",
        'alarm_from_address': "root@localhost",
        'SMTP_server': 'smtp.gmail.com:587',
        'SMTP_username' : '',
        'SMTP_password' : '',
    }
    
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
