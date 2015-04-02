#!/usr/bin/env python
#

# Recieve strings and display on phidgets LCD module

'''
Borrowed and Modified from the Phidgets example code by Adam Stelmack.

Basic LCD communication
'''

__author__ = 'Cameron Rodda'
__version__ = '0.0.2'
__date__ = '10 August 2013'

from ctypes import *
import sys
from time import sleep
import zmq

#Phidget specific imports
from Phidgets.Phidget import PhidgetID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize
#from Phidgets.Devices.InterfaceKit import InterfaceKit

#Create an TextLCD object
try:
    textLCD = TextLCD()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#try:
#    interfaceKitLCD = InterfaceKit()
#except RuntimeError as e:
#    print("Runtime Exception: %s" % e.details)
#    print("Exiting....")
#    exit(1)

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
#    interfaceKitLCD.openPhidget(serial=120517)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)    

#Wait for the device to attach
try:
    textLCD.waitForAttach(10000)
#    interfaceKitLCD.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        textLCD.closePhidget()
#        interfaceKitLCD.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)    

textLCD.setBacklight(True)
textLCD.setBrightness(128)

print("lcd setup complete, ready for use")

context = zmq.Context()

lcd_receiver = context.socket(zmq.PULL)
lcd_receiver.bind("ipc:///tmp/lcd.ipc")
print("PULL socket complete on ipc://tmp/lcd.ipc")

#relay_receiver = context.socket(zmq.SUB)
#relay_receiver.bind("ipc:///tmp/shaft.ipc")
#relay_receiver.setsockopt(zmq.SUBSCRIBE, "") #subscribe to all messages
#relay_receiver.setsockopt(zmq.RCVTIMEO, 500) #set a timeout of 500ms for a receive operation (prevent hangs)
#print("SUB socket complete on ipc://tmp/shaft.ipc")

#The MEAT goes here...

while True:
    print("going into forever loop mode")

    #first collect shaft movement messages...  
    #try:
    #    relayed = relay_receiver.recv_json()
    #    print(result)

       
    #Then worry about displaying messages on the LCD...
    result = lcd_receiver.recv_json()
    print(result)
    #print result['message'],result['line'],result['delay']

    if 'message' in result:
        try:
            #clear the specified line...
            textLCD.setDisplayString(int(result['line']),"")
            #print the required text...
            textLCD.setDisplayString(int(result['line']),str(result['message']))
        
            if 'delay' in result:
                print("Waiting for Delay...")
                sleep(int(result['delay']))


        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)


#    if 'up' in result:
#        interfaceKitLCD.setOutputState(0,True)
#        interfaceKitLCD.setOutputState(1,False)#

#        sleep(int(result['up']))

#        interfaceKitLCD.setOutputState(0,False)
#        interfaceKitLCD.setOutputState(1,False)

#    elif 'down' in result:
#        interfaceKitLCD.setOutputState(0,False)
#        interfaceKitLCD.setOutputState(1,True)

#        sleep(int(relayed['down']))

#        interfaceKitLCD.setOutputState(0,False)
#        interfaceKitLCD.setOutputState(1,False)

#    else:
        #default to stop moving to avoid colisions
#        interfaceKitLCD.setOutputState(0,False)
#        interfaceKitLCD.setOutputState(1,False)


#print("Press Enter to quit....")

#chr = sys.stdin.read(1)

#print("Closing...")

textLCD.setDisplayString(0, "")
textLCD.setDisplayString(1, "")
textLCD.setBacklight(False)

#try:
#    textLCD.closePhidget()
#except PhidgetException as e:
#    print("Phidget Exception %i: %s" % (e.code, e.details))
#    print("Exiting....")
#    exit(1)

#print("Done.")
#exit(0)

