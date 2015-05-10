Australian-Synchrotron-Surveyor-Tunnel-Exploration-And-Fault-Detection-Robot
=======

Australian Synchrotron Tunnel Bot
![](https://raw.github.com/AustralianSynchrotron/Australian-Synchrotron-Surveyor-Tunnel-Exploration-And-Fault-Detection-Robot/master/drawings/logos/RoboDonkey.png)

###Requirements
------------

1. Python 2.7.x
2. ZeroMQ 3.2.x
3. pyzmq  13.1.0
4. Pyserial
5. libphidget LATEST (currently 2.1.8.20130723)
6. libusb 1.0-0
7. mjpg-streamer experimental
8. cherrypy 3.2.x
9. Arduino 1.5
-- PS2X by Bill Porter
10. supervisor 3.0b2-1
11. ROOter Huntsman 2014-01-25red


###Changes
-------

ipc doesn't seem to be working on this current configuration (except for LCD screen) so motors and IR Sensors using zmq on tcp://127.0.0.2
ports:
irsensor 127.0.0.2:1000
motors 127.0.0.2:1100


note: srv_motor.py now has the bind command for the motors zmq socket, since it is the service which is always running. If testing run py script with sudo

###Command Line
--------

ssh to odroid. The following command line scripts can be used for some low level control of ass-bot

**move** *\<direction\> \<duration\> \<speed\>*

* direction: forward (f), back (b), left (l), right (r)

* duration: time of movement in seconds

* speed: percentage of max speed. From 0 to 100

**shaft** *\<direction\> \<duration\>*

* direction: up or down (written in full)

* duration: time of movement in seconds

**camera** *\<direction\> \<PWM duration\>*

* direction: Pan (p) or tilt (t)

* PWM duration: Pulse width from 500 to 2500. Form tilt centre value is 900, for pan centre value is 1500
