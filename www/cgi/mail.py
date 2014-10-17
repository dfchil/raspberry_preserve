#!/usr/bin/env python
# encoding: utf-8

import sys
import time
import pconfig
import smtplib
import cgi

def send_warning(descr, value, cfg, toaddrs=None):
    # Specifying the from and to addresses
    from_address = cfg.get('settings', 'alarm_from_address');
    if toaddrs == None:
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
    server.sendmail(from_address, toaddrs.split(";"), header + message)
    server.quit()



def webreq(form):
    cfg = pconfig.read('rb_preserve.cfg')
    try:
        sndto = form.getvalue('alarm_to_addresses')
        send_warning("Test", "-1.0", cfg, toaddrs=sndto)
        return "".join([ "Test mail successfully sent to the following recipients:\n",
        sndto.replace(";", "\n")])
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    print "Content-type:text/html\r\n\r\n%s" % webreq(form)
