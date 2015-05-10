#!/usr/bin/env python
#

#import sys
#import lib_pololu
#import serial

import zmq
import sys

#port = serial.Serial('/dev/ttyACM0')
#port.baudrate=9600

#camera_pan = lib_pololu.Servo(port,0,1150,4650)
#camera_tilt = lib_pololu.Servo(port,1,1150,4650)

#camera_pan.set_pos(80)
#camera_tilt.set_pos(0)

#camera_pan.set_neutral()
#camera_tilt.set_neutral()

context = zmq.Context()
servo_socket = context.socket(zmq.PUB)
servo_socket.connect("ipc:///tmp/servo.ipc")

def send_servo(servo,duration):
    if (servo == "0") or (servo == 0):
        msg = {"servo:00:pan":duration}

    elif (servo == "1") or (servo == 1):
        msg = {"servo:01:tilt":duration}

    else:
        msg = {"servo:00:pan":"1500",
                "servo:01:tilt":"1500"}

    print("sending message: %s" % msg)
    servo_socket.send_json(msg)

    sys.exit(21)

if __name__ == "__main__":
    #if len(sys.argv) > 0:
    servo = sys.argv[1]
    duration = sys.argv[2]
    #except:
    #    pass
    print("%s: %s" % (servo,duration))
    send_servo(servo,duration)
