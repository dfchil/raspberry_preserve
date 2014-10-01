#!/usr/bin/env python
# encoding: utf-8


import plot
import pconfig

if __name__ == "__main__":
    
    cfg = pconfig.read('rb_preserve.cfg')
    print """Content-Type: application/javascript

function min_secs(){
    return %f;
}

function default_begin(){
    return %d;
}
    """ % (plot.first_entry(cfg.get('settings', 'timeformat')) *1000, 
    int(cfg.get('settings', 'default_view_hours')))
