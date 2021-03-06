#!/usr/bin/env python

'''
Borrowed and Modified from the Phidgets example code by Adam Stelmack.

Basic LCD communication
'''

__author__ = 'Cameron Rodda'
__version__ = '0.0.1'
__date__ = '30 July 2013'

from ctypes import *
import sys
from time import sleep
#Phidget specific imports
from Phidgets.Phidget import PhidgetID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize

#Create an TextLCD object
try:
    textLCD = TextLCD()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

def TextLCDError(e):
    try:
        source = e.device
        print("TextLCD %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))


#Connect the event handlers
try:
    textLCD.setOnErrorhandler(TextLCDError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)      

#Open the textLCD
try:
    textLCD.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)    

#Wait for the device to attach
try:
    textLCD.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        textLCD.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)    

try:
    textLCD.setScreenIndex(0)

    #print("Writing to first row....")
    textLCD.setDisplayString(0, "Initialising...")
    sleep(2)

    textLCD.setBacklight(True)
    textLCD.setBrightness(128)

    #print("Writing to second row....")
    textLCD.setDisplayString(1, "Complete!")
    sleep(2)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)


print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

textLCD.setDisplayString(0, "")
textLCD.setDisplayString(1, "")
textLCD.setBacklight(False)

try:
    textLCD.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)