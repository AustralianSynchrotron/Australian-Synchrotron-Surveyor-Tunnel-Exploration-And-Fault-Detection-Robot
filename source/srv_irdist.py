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
    interfaceKitHUB = InterfaceKit()
    #interfaceKitLCD = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKitHUB.isAttached(), interfaceKitHUB.getDeviceName(), interfaceKitHUB.getSerialNum(), interfaceKitHUB.getDeviceVersion()))
#    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKitLCD.isAttached(), interfaceKitLCD.getDeviceName(), interfaceKitLCD.getSerialNum(), interfaceKitLCD.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKitHUB.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKitHUB.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKitHUB.getSensorCount()))

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

def interfaceKitHUBInputChanged(e):
    global bumper_socket
    source = e.device

    if e.index == 0:
        if e.state:
            msg = {"nw": "1"}
        else:
            msg = {"nw": "0"}

    if e.index == 1:
        if e.state:
            msg = {"n": "1"}
        else:
            msg = {"n": "0"}

    if e.index == 2:
        if e.state:
            msg = {"ne": "1"}
        else:
            msg = {"ne": "0"}

    if e.index == 3:
        if e.state:
            msg = {"sw": "1"}
        else:
            msg = {"sw": "0"}

    if e.index == 4:
        if e.state:
            msg = {"s": "1"}
        else:
            msg = {"s": "0"}

    if e.index == 5:
        if e.state:
            msg = {"se": "1"}
        else:
            msg = {"se": "0"}

    bumper_socket.send_json(msg)

    print("InterfaceKitHUB %i: Input %i: %s... message: %s" % (source.getSerialNum(), e.index, e.state, msg))

#def interfaceKitLCDInputChanged(e):
#    source = e.device
#    print("InterfaceKitLCD %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

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
#    interfaceKitHUB.setOnAttachHandler(interfaceKitAttached)
#    interfaceKitHUB.setOnDetachHandler(interfaceKitDetached)
    interfaceKitHUB.setOnErrorhandler(interfaceKitError)
    interfaceKitHUB.setOnInputChangeHandler(interfaceKitHUBInputChanged)
#    interfaceKitHUB.setOnOutputChangeHandler(interfaceKitOutputChanged)
#    interfaceKitHUB.setOnSensorChangeHandler(interfaceKitSensorChanged)

#    interfaceKitLCD.setOnAttachHandler(interfaceKitAttached)
#    interfaceKitLCD.setOnDetachHandler(interfaceKitDetached)
#    interfaceKitLCD.setOnErrorhandler(interfaceKitError)
#    interfaceKitLCD.setOnInputChangeHandler(interfaceKitLCDInputChanged)
#    interfaceKitLCD.setOnOutputChangeHandler(interfaceKitOutputChanged)
#    interfaceKitLCD.setOnSensorChangeHandler(interfaceKitSensorChanged)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
# Open interfaceKit by serial number to avoid conflicts with future interface kits...
# As displayed by displayDeviceInfo()
#    interfaceKitLCD.openPhidget(serial=120517)
    interfaceKitHUB.openPhidget(serial=337662)
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    interfaceKitHUB.waitForAttach(10000)
    #interfaceKitLCD.waitForAttach(10000)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKitHUB.closePhidget()
        #interfaceKitLCD.closePhidget()
        
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

#print("Setting the data rate for each sensor index to 4ms....")
for i in range(interfaceKitHUB.getSensorCount()):
    try:
        interfaceKitHUB.setDataRate(i, 2)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print "\n"

#Make sure the ratiometric setting is set (required by sonar)
if not interfaceKitHUB.getRatiometric:
    interfaceKitHUB.setRatiometric(True)

#Register interupt callback
signal.signal(signal.SIGINT, signal_handler)

#Setup zmq sockets
context = zmq.Context()
distance_socket = context.socket(zmq.PUB)
distance_socket.setsockopt(zmq.LINGER, 100)
distance_socket.bind("ipc:///tmp/distance.ipc")
#distance_socket.bind("tcp://127.0.0.2:1000")

bumper_socket = context.socket(zmq.PUB)
bumper_socket.setsockopt(zmq.LINGER, 100)
bumper_socket.bind("ipc://tmp/bumper.ipc")

##########################################################
#
#		S (rear)
#		---------
#		|	|
#		|	|
# E (right)	|	|	W (left)
#		|	|
#		|	|
#		---------
#
#		N (front)
#
##########################################################


array = ["ne","e","se","nw","w","sw","front","rear"]

#print out the array distance...
#seems to be accurate to around +/-2mm

while True:
    message = []

    if interupt:
        print('Interupt: Shutting down script...')
        #try and shut down the interface kits
        try:
            interfaceKitHUB.closePhidget()
            #interfaceKitLCD.closePhidget()

        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        print("Done.")
        exit(2)
        break

    for i in range(interfaceKitHUB.getSensorCount()):
        try:
            #intval = interfaceKitHUB.getSensorValue(i)
            #if 0 reading, don't try and convert
            #if not intval:
            #    continue

            if i >= 6:
                #Sonar sensor range 0cm - 645cm
                #Plugged into analog input 6 & 7 for N (forward) and S (reverse)

                #turn on the sonar sensor via digital output 'i'
                interfaceKitHUB.setOutputState(i,True)
                #intval = interfaceKitHUB.getSensorValue(i)
                #sleep(0.1) # Wait for sonar to activate
                intval = interfaceKitHUB.getSensorRawValue(i) #Read sonar
                print intval, i
                distance_mm = (intval / 4.095 ) * 12.96 #convert raw value to mm
                #Check that value is within permissable range
                if distance_mm > 6450.0:
                    distance_mm = -1

                #turn off the sonar sensor via digital output 'i'
                interfaceKitHUB.setOutputState(i,False)
                sleep(0.4)
                #save value into array
                #message.append(distance_mm)
            else:
                #IR range 20cm - 150cm (2.5V - 0.4V)
                #Read seonsor value
                intval = interfaceKitHUB.getSensorRawValue(i)
                print intval
                #convert raw value to mm
                distance_mm = (9462/((intval / 4.095) - 16.92)) * 10
                #Not a reliable mesaurement below 200mm (20cm) or above 1500 (150cm)
                if (distance_mm < 200.0) or (distance_mm > 1500.0):
                    distance_mm = -1
                sleep(0.4)

                #save value into array
                #message.append(distance_mm)

	    #message.append("%s: %s," % (array[i], distance_mm))
	    message.append(distance_mm)

            print( "Distance - Device %i: %smm" % ( i, distance_mm ) )
            print( message )
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
    print("==============================")
    sleep(0.2)

    #msg = {'front': '32.543'}
    #Export distance array via json to ipc://distance.ipc
    msg = dict(zip(array,message))
    print("Sending Message: %s" % msg )
    print("==============================")
    distance_socket.send_json(msg)
#print "Sensor ValueHUB",interfaceKitHUB.getSensorValue(0)
#print "Sensor ValueLCD",interfaceKitLCD.getSensorValue(0)

#print interfaceKitHUB.getRatiometric()

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKitHUB.closePhidget()
    #interfaceKitLCD.closePhidget()

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)

