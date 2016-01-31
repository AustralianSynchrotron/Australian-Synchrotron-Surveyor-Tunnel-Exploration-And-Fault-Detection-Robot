#!/usr/bin/env python
#

from time import sleep
from datetime import datetime
import commands
import signal
import sys
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("ipc:///tmp/shaft.ipc")
print("connected to socket shaft.ipc")

while True:
   dirval = raw_input('Direction (up/down):')
   durval = raw_input('Duration (s):')
   msg={dirval:durval}
   print("sending message %s", msg)
   zmq_socket.send_json(msg)






