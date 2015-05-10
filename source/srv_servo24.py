#!/usr/bin/env python
#

"""
Borrowed and modified from the phidgets example code by Adam Stelmack
http://creativecommons.org/licenses/by/2.5/ca/
"""


#import time
import sys
import zmq

#Basic imports
from ctypes import *
from time import sleep

#Servo imports
import mod_servo_device as device

servo_control = device.Device()
print("Current Servo positions: %s" % servo_control.get_positions([0, 1]))
#neutral_cam_platform = [1500, 1500] #set the neutral position for the 2 camera servos on the platform
#servo_control.set_targets(2,0,neutral_cam_platform)

#set some basic movement parameters...
servo_control.set_speeds([0,1],[10,10])
servo_control.set_acceleration(0,1) #servo, acc
servo_control.set_acceleration(1,1) #servo,acc

print('servo24 setup complete, ready for use')

#Setup zmq sockets
context = zmq.Context()
servo_socket = context.socket(zmq.SUB)
servo_socket.bind("ipc:///tmp/servo.ipc")
servo_socket.setsockopt(zmq.SUBSCRIBE, "") #subscribe to all messages
print("SUB socket complete on ipc://tmp/servo.ipc")


# Message is expected to be either "servo:00:pan" or "servo:01:tilt" 
# for the top platform mounted camera gizmo
# The value for the dict entry is a setting in micro seconds in the range {250:2750}
# a value of 1500 is considered neutral
def processCmd(message):
    global servo_control
    if "servo:00:pan" in message:
        val = int(message["servo:00:pan"])
        servo_control.set_target(0,val)
        print("Moving servo 0 to position: %s" % val)
        err = servo_control.get_errors()
        if err:
            print("An error has been detected: %s" % err)

    if "servo:01:tilt" in message:
        val = int(message["servo:01:tilt"])
        servo_control.set_target(1,val)
        print("Moving servo 1 to position: %s" % val)
        err = servo_control.get_errors()
        if err:
            print("An error has been detected: %s" % err)


while True:

    try:
        print("Waiting for message... on servo.ipc")
        msg = servo_socket.recv_json()
        print(msg)


        processCmd(msg) #process the recieved message


    except KeyboardInterrupt:
        print('Exiting...')
        servo_control.con.flush() #flush the serial connection
        servo_control.con.close() #close the serial connection
        exit(2)

    except:
        print("nothing received... waiting")
        pass

print("Done.")
exit(0)

