Raspberry Preserve
==================

Climate measuring software for the Raspberry Pi

The requirements for this project came from the Conservation department at 
Statens Museum for Kunst. They required a way to check the temperature and 
humidity of certain rooms containing fragile artworks from a remote location.

Goals:

* Sample temperature and moisture at given interval
* Store data for statistical purposes
* Generate alarms if over certain threshold (Send e-mail)
* Generate plots from stored data

You can get an impression how it looks like a the [Demo Server](http://ndrx.net/raspberry_preserve/)


Installation
------------

### Hardware

This project was developed and tested on a Raspberry Pi version B+, it
should also run on the classical version B and the newer Raspberry 
Pi 2. If you only need Wi-Fi and no Ethernet (cable LAN) you can also 
use the cheaper version A or A+. This project uses a combined temperature/
humidity sensor from the DHT series or a AM2302. Connect the data out 
pin of the sensor to GPIO pin 4 of the [Raspberry Pi expansion port](http://elinux.org/RPi_Low-level_peripherals#General_Purpose_Input.2FOutput_.28GPIO.29).

Pinning of the DHT/AM2302 Sensor (from left to right):

* VCC (3.3V power)
* Data out
* Not connected
* Ground

For DHT11 and DHT22 sensors, don't forget to connect a 4.7K - 10K 
resistor from the data pin to VCC. If 4.7K doesn't work, try 10K.


### Base install of the operating system

This project was done using the official Raspian Wheezy image. So you first 
have to download and install Raspian to your Raspberry Pi.

Go to [raspberrypi.org](https://www.raspberrypi.org/downloads/raspbian/) and 
download the newest Wheezy image. Jessie should also work but is not tested yet.

Then follow the [installation instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
and then connect your device to the network and test it. 

With the command line tool `raspi-config` enable the SSH server and try if you
are able to log in. This device will be placed in some remote location so you 
would like to be able to maintain it over the network.


### Install raspberry_preserve

1. First make a SSH connection to your Raspberry Pi.

2. Follow this instructions to install the Adafruit DHT library for Python and
to test your sensor connection. The source code is included in this project, 
so you can skip the step to download the library:
[Adafruit: Humidity Sensing on Raspberry Pi or Beaglebone](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated)


3. Install additional needed software and get the raspberry_preserve code:

	    sudo apt-get install gnuplot lighttpd python-flup
	    cd /home/pi/
	    git clone https://github.com/daniel-fairchild/raspberry_preserve.git

4. Configure the web server lighttpd:

    First we configure lighttpd to be able to execute Python code:

	    sudo cp raspberry_preserve/configuration/10-fastcgi.conf /etc/lighttpd/conf-available/

    Next we replace the normal web server data folder with a link to the 
    www folder inside the project. We do this because it makes it much easier 
    to upgrade the raspberry_preserve software:

	    sudo rm -r /var/www
	    sudo ln -s raspberry_preserve/www /www

    Create the data directory and make it writable for the web server:

	    mkdir raspberry_preserve/www/cgi/data
	    sudo chown www-data:www-data /home/pi/raspberry_preserve/www/cgi/data

5. Create the configuration file `rb_preserve.cfg`:

	    cp raspberry_preserve/configuration/rb_preserve.cfg.sample raspberry_preserve/www/cgi/rb_preserve.cfg
	    sudo chown www-data:www-data raspberry_preserve/www/cgi/rb_preserve.cfg

    Edit the configuration file and fill in the basic information:

	    sudo nano raspberry_preserve/www/cgi/rb_preserve.cfg

    Finally restart the web server:

	    sudo /etc/init.d/lighttpd restart

6. Install cronjob to execute poll.py every minute:
    The script poll.py reads the sensors, processes the data (averaging) and 
    sends e-mails in the event an alarm threshold is reached.

	    sudo cp /home/pi/raspberry_preserve/configuration/raspberry_preserve /etc/cron.d
	    sudo /etc/init.d/cron restart

7. Wait some minutes and check if everything is working.

    Check the immediate data file. It should contain some sensor values:

	    cat /run/shm/intermediary.data

    Do the same for the averaged sensor data stored on the SD card. You get a seperate file for every month:

	    ls -l /home/pi/raspberry_preserve/www/cgi/data/
	    cat /home/pi/raspberry_preserve/www/cgi/data/<insert here your fresh data file>

    Open a web browser, enter the IP address of your Raspberry Pi and see if the
    plotting of your data works.

Updates
-------

To update your raspberry_preserve installation, you just have to update the local git repository:

    cd /home/pi/raspberry_preserve
    git update


Implementation
--------------

* Data gathering through cron triggered python script 
* Above script also triggers alarms
* Store in flat CVS file. Format: datetime, moisture, temperature
* Generate plots with gnuplot
