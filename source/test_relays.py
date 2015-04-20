#!/usr/bin/env python
#

import time
import commands
import signal
import sys
import zmq

interupt = False

def signal_handler(signum, frame):
    global interupt
    interupt = True


context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.connect("ipc:///tmp/shaft.ipc")
print("connected to socket shaft.ipc")
print("===================================================")
print("|       Must be run as root! Just Say'n           |")
print("===================================================")
print("")
print("Usage: test_relays.py [direction<string> {'up'|'down'}] [seconds_of_movement<string> {'1'|'2'|'3'|'4'|'5'... etc}]")
print("")
dir = sys.argv[1]
len = sys.argv[2]

def send_message(dir,len):
    msg={dir:len}
    print("moving for %s seconds" % msg[dir])

    print("sending message %s", msg)
    zmq_socket.send_json(msg)

    #print("sleeping 1")
    #time.sleep(5)

    sys.exit()

if __name__ == "__main__":
    send_message(dir,len)
    

