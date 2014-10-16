#!/usr/bin/env python
# encoding: utf-8

import plot
import pconfig
import json

def webreq():
    
    cfg = pconfig.read('rb_preserve.cfg')    
    first_value, last_value = plot.data_span()
    
    return """
function min_secs(){
    return %f;
}

function max_secs(){
    return %f;
}

function default_begin(){
    return %s;
}

function config_json(){
    return %s;
}
""" % (first_value *1000, last_value *1000,
    cfg.get('settings', 'default_view_hours'),
    pconfig.json_out())


if __name__ == "__main__":
    print "Content-type:application/javascript\r\n\r\n%s" % webreq()