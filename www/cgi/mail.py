#!/usr/bin/env python
# encoding: utf-8

import sys
import time
import pconfig
import smtplib

def send_warning(descr, value, cfg):
    # Specifying the from and to addresses
    from_address = cfg.get('settings', 'alarm_from_address');
    toaddrs  = cfg.get('settings', 'alarm_to_addresses');
    node_name = cfg.get('settings', 'node_name');
    node_description = cfg.get('settings', 'node_description');
    node_netaddress =  cfg.get('settings', 'node_netaddress');
    interval =  cfg.get('settings', 'sample_period');

    header = """From: %s
To: %s
Subject: %s warning from %s


"""  % (from_address, toaddrs, descr, node_name)
    message = """
%s of %.2f measured on %s as an average over the last %d minutes.

%s has the following description: %s

Browse the data historiy of %s at: 
%s . 

""" %(descr, float(value), node_name, int(interval), 
    node_name, node_description,
    node_name, node_netaddress)

    # Gmail Login
    username = cfg.get('settings', 'smtp_username');
    password = cfg.get('settings', 'smtp_password');

    # Sending the mail  
    server = smtplib.SMTP(cfg.get('settings', 'smtp_server'))
    server.starttls()
    
    if len(username) > 0 and len(password) > 0:
        server.login(username,password)
    server.sendmail(from_address, toaddrs, header + message)
    server.quit()

def main(argv=None):    
    cfg = pconfig.read('rb_preserve.cfg')
    send_warning("Test", "-1.0", cfg)

if __name__ == "__main__":
    sys.exit(main())
