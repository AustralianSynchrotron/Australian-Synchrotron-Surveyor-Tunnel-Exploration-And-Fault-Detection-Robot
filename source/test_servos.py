#!/usr/bin/env python
#

import sys
import lib_pololu
import serial

port = serial.Serial('/dev/ttyACM0')
port.baudrate=9600

camera_pan = lib_pololu.Servo(port,0,1150,4650)
camera_tilt = lib_pololu.Servo(port,1,1150,4650)

camera_pan.set_pos(80)
camera_tilt.set_pos(0)

camera_pan.set_neutral()
camera_tilt.set_neutral()
