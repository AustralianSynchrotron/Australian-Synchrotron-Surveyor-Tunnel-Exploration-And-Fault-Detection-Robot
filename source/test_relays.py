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



msg={"up":"3"}
print("moving for %s seconds" % msg['up'])

print("sending message %s", msg)
zmq_socket.send_json(msg)

#print("sleeping 1")
#time.sleep(5)

sys.exit()
