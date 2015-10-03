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
