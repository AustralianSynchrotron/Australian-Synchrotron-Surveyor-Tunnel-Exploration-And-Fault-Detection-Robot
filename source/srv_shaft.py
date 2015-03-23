#!/usr/bin/env python
#

"""
Borrowed and modified from the phidgets example code by Adam Stelmack
http://creativecommons.org/licenses/by/2.5/ca/
"""


import time
import sys
import zmq

#Basic imports
from ctypes import *
from time import sleep
#import sys
import random
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

import signal

interupt = False

def signal_handler(signum, frame):
    global interupt
    interupt = True

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


def interfaceKitLCDInputChanged(e):
    source = e.device
    print("InterfaceKitLCD %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
    source = e.device
#    print e.rawValue
    try:
        if e.index >= 6:
            #Sonar sensor range 0cm - 645cm
            #Plugged into analog input 6 & 7 for N (forward) and S (reverse)
            distance_mm = e.value * 12.96
            if distance_mm > 6450.0:
                distance_mm = "NaN"

        else:
            #IR range 20cm - 150cm
            distance_mm = (9462/(e.value - 16.92)) * 10
            #Not a reliable mesaurement below 200mm (20cm) or above 1500 (150cm)
            if (distance_mm < 200.0) or (distance_mm > 1500.0):
                distance_mm = "NaN"

        print( "Distance - Device %i: %smm" % ( e.index, distance_mm ) )
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

#Main Program Code
try:

    interfaceKitLCD.setOnErrorhandler(interfaceKitError)
    interfaceKitLCD.setOnInputChangeHandler(interfaceKitLCDInputChanged)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
# Open interfaceKit by serial number to avoid conflicts with future interface kits...
# As displayed by displayDeviceInfo()
    interfaceKitLCD.openPhidget(serial=120517)

    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

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

#Register interupt callback
signal.signal(signal.SIGINT, signal_handler)

#Setup zmq sockets
context = zmq.Context()
shaft_socket = context.socket(zmq.SUB)
shaft_socket.bind("ipc:///tmp/shaft.ipc")


while True:
    message = []

    if interupt:
        print('Interupt: Shutting down script...')
        #try and shut down the interface kits
        try:
            interfaceKitLCD.closePhidget()

        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        print("Done.")
        exit(2)
        break


    #Export distance array via json to ipc://distance.ipc
    msg = dict(zip(array,message))
    print("Sending Message: %s" % msg )
    print("==============================")
    distance_socket.send_json(msg)

#print "Sensor ValueLCD",interfaceKitLCD.getSensorValue(0)

#print interfaceKitHUB.getRatiometric()

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKitHUB.closePhidget()
    interfaceKitLCD.closePhidget()

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)

