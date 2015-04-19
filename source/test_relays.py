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
    

