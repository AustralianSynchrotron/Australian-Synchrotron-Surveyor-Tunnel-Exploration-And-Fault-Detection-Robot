Australian-Synchrotron-Surveyor-Tunnel-Exploration-And-Fault-Detection-Robot
=======

Australian Synchrotron Tunnel Bot
![](https://raw.github.com/AustralianSynchrotron/Australian-Synchrotron-Surveyor-Tunnel-Exploration-And-Fault-Detection-Robot/master/drawings/logos/RoboDonkey.png)

###Requirements
------------

1. Python 2.7.x
2. ZeroMQ 3.2.x
3. pyzmq  13.1.0
4. libphidget LATEST (currently 2.1.8.20130723)
5. libusb 1.0-0
6. mjpg-streamer experimental
7. cherrypy 3.2.x
8. Arduino 1.5
-- PS2X by Bill Porter
9. supervisor 3.0b2-1
10. ROOter Huntsman 2014-01-25red


###Changes
-------

ipc doesn't seem to be wlorking on this current configuration (except for LCD screen) so motors and IR Sensors using zmq on tcp://127.0.0.2
ports:
irsensor 1000
motors 1100


note: srv_motor.py now has the bind command for the motors zmq socket, since it is the service which is always running.



