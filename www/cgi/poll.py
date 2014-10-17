#!/usr/bin/env python
# encoding: utf-8

import sys
import time
import os
import pconfig
import mail

# def send_warning(descr, value, cfg):
#     # Specifying the from and to addresses
#     from_address = cfg.get('settings', 'alarm_from_address');
#     toaddrs  = cfg.get('settings', 'alarm_to_addresses');
#     node_name = cfg.get('settings', 'node_name');
#     node_description = cfg.get('settings', 'node_description');
#     node_netaddress =  cfg.get('settings', 'node_netaddress');
#     interval =  cfg.get('settings', 'sample_period');
#
#     header = """From: %s
# To: %s
# Subject: %s warning from %s
#
#
# """  % (from_address, toaddrs, descr, node_name)
#     message = """
# %s of %.2f measured on %s as an average over the last %d minutes.
#
# %s has the following description: %s
#
# Browse the data historiy of %s at:
# %s .
#
# """ %(descr, float(value), node_name, int(interval),
#     node_name, node_description,
#     node_name, node_netaddress)
#
#     # Gmail Login
#     username = cfg.get('settings', 'smtp_username');
#     password = cfg.get('settings', 'smtp_password');
#
#     # Sending the mail
#     server = smtplib.SMTP(cfg.get('settings', 'smtp_server'))
#     server.starttls()
#
#     if len(username) > 0 and len(password) > 0:
#         server.login(username,password)
#     server.sendmail(from_address, toaddrs, header + message)
#     server.quit()

def poll():
    sensor = Adafruit_DHT.AM2302
    pin = 4
    return Adafruit_DHT.read_retry(sensor, pin)

def warning_test(humidity, temperature, cfg):
    #if humidity outside range
    if humidity < float(cfg.get('settings', 'humidity_min')):
        mail.send_warning("Low humidty", humidity, cfg)
    if humidity > float(cfg.get('settings', 'humidity_max')):
        mail.send_warning("High humidty", humidity, cfg)
        
    if temperature > float(cfg.get('settings', 'temperature_max')):
        mail.send_warning("High temperature", temperature, cfg)
        


def condense(tmplnes):
    td = []
    for lt in tmplnes:
        try:
            h, t = lt.split(',')
            h = float(h)
            t = float(t)
            td.append((h,t))
        except:
            continue
    tmplnes = []
    th = 0.0;
    tt = 0.0;
    for i in range(len(td)):
        th += td[i][0]
        tt += td[i][1]

    th /= len(td)
    tt /= len(td)
    return (th, tt)

def main(argv=None):    
    cfg = pconfig.read('rb_preserve.cfg')

    ddir = cfg.get('settings', 'data_dir')
    timeformat = pconfig.dformat();
    pwd = os.path.dirname(os.path.realpath(__file__))
    
    #sample sensor
    humidity = None
    temperature = None
    
    while humidity == None and temperature == None:
        humidity, temperature = poll()

    # see if 
    tmpfn = os.path.join(cfg.get('settings', 'tmp_dir'), "intermediary.data")

    if os.path.exists(tmpfn):
        with open(tmpfn, 'r') as pd:
            lines = pd.readlines()
    else:
        lines = []
    
    lines.append("%.2f,%.02f\n" % (humidity, temperature))
    
    if len(lines) >= int(cfg.get('settings', 'sample_period')):        
        avg_hum, avg_temp = condense(lines)
        warning_test(avg_hum, avg_temp, cfg)
        lines = []   # zerro tmp file
        
        #store in persistent file
        pfname = "%s/%s/%s.data" % (pwd, ddir, time.strftime(pconfig.dfilename_fmt()))
        pstr = "%s,%.2f,%.02f\n" % (time.strftime(timeformat), avg_hum, avg_temp)
        with open(pfname, "a") as outfile:
            outfile.write(pstr)

    #overwrite existing tmp file with current data
    with open(tmpfn, 'w') as pd:
        pd.write("".join(lines))

if __name__ == "__main__":
    import Adafruit_DHT
    sys.exit(main())
