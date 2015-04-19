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
#import sys
import random
#Phidget specific imports
from Phidgets.Phidget import PhidgetID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

#Create an interfacekit object
try:
    interfaceKitLCD = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKitLCD.isAttached(), interfaceKitLCD.getDeviceName(), interfaceKitLCD.getSerialNum(), interfaceKitLCD.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKitLCD.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKitLCD.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKitLCD.getSensorCount()))

#Event Handler Callback Functions
def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))


def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

#Main Program Code
try:
    interfaceKitLCD.setOnErrorhandler(interfaceKitError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
# Open interfaceKit by serial number to avoid conflicts with future interface kits...
# As displayed by displayDeviceInfo()
    interfaceKitLCD.openRemote('odroid',serial=120517)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

if not interfaceKitLCD.isAttachedToServer():
    sleep(2)

print('interfaceKitLCD attached to server: %s' % interfaceKitLCD.isAttachedToServer())

#wait for the device to attach
try:
    interfaceKitLCD.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKitLCD.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print('lcd setup complete, ready for use')

#Setup zmq sockets
context = zmq.Context()
shaft_socket = context.socket(zmq.SUB)
shaft_socket.bind("ipc:///tmp/shaft.ipc")
shaft_socket.setsockopt(zmq.SUBSCRIBE, "") #subscribe to all messages
print("SUB socket complete on ipc://tmp/shaft.ipc")

while True:

    try:
        relayed = shaft_socket.recv_json()
        print(relayed)


        if 'down' in relayed:
            interfaceKitLCD.setOutputState(0,True)
            interfaceKitLCD.setOutputState(1,False)
            print("going Down")
            sleep(int(relayed['down']))

            interfaceKitLCD.setOutputState(0,False)
            interfaceKitLCD.setOutputState(1,False)

        elif 'up' in relayed:
            interfaceKitLCD.setOutputState(0,False)
            interfaceKitLCD.setOutputState(1,True)
            print("going Up")
            sleep(int(relayed['up']))

            interfaceKitLCD.setOutputState(0,False)
            interfaceKitLCD.setOutputState(1,False)

        else:
            #default to stop all motion to avoid collisions
            interfaceKitLCD.setOutputState(0,False)
            interfaceKitLCD.setOutputState(1,False)

    except KeyboardInterrupt:
        print('Exiting...')
        interfaceKitLCD.closePhidget()
        exit(2)

    except:
        print("nothing received... waiting")
        pass

try:
    interfaceKitLCD.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)

