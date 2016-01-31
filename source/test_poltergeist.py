#!/usr/bin/env python
#

from time import sleep
from datetime import datetime
import commands
import signal
import sys
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.connect("ipc:///tmp/shaft.ipc")
print("connected to socket shaft.ipc")

while True:
    try:
        tnow = datetime.now()

        if tnow.minute == 13:
            msg={'down':'2'}
            print("moving for %s seconds" % msg['down'])
            print("sending message %s", msg)
            zmq_socket.send_json(msg)

        elif tnow.minute == 38:
            msg={'up':'1'}
            print("moving for %s seconds" % msg['up'])
            print("sending message %s", msg)
            zmq_socket.send_json(msg)
        else:
            print("nothing to do... %s" % tnow.minute)
            pass

        

        sleep(50)

    except KeyboardInterrupt:
        exit(1)

sys.exit()
 

