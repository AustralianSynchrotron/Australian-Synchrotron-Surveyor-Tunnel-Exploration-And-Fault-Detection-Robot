#!/usr/bin/env python
#

# Collect system variables and send to display and other ports


__author__ = 'Cameron Rodda'
__version__ = '0.0.1'
__date__ = '21 August 2013'

import commands
import zmq
import time
from ctypes import *
import sys
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, InputChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.MotorControl import MotorControl

#Create a motor control object
try:
    mcL = MotorControl() # Left Motor
    mcR = MotorControl() # Right Motor
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

try:
    #mcL.openPhidget(serial=298857)
    #mcR.openPhidget(serial=298856)
    mcL.openRemote('odroid',serial=298857)
    mcR.openRemote('odroid',serial=298856)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:
    mcL.waitForAttach(10000)
    mcR.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        mcL.closePhidget()
        mcR.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

print("mcL attached to WebService: %s" % mcL.isAttachedToServer())
print("mcR attached to WebService: %s" % mcR.isAttachedToServer())

context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind("ipc:///tmp/battery.ipc")


while True:
    
    bat1 = mcL.getSupplyVoltage()
    bat2 = mcR.getSupplyVoltage()

    print("Battery1: %s, Battery2: %s" % (bat1, bat2))
    msg = {'battery1': bat1, 'battery2': bat2}
    zmq_socket.send_json(msg)
    time.sleep(10.0) #battery voltage only changes relatively slowly - no need for great update rate
