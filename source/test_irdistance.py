#!/usr/bin/env python
#

import zmq
import time
import commands

context = zmq.Context()
zmq_socket = context.socket(zmq.SUB)
zmq_socket.connect("ipc:///tmp/distance.ipc")
zmq_socket.setsockopt(zmq.SUBSCRIBE, '') #recv all messages

while True:
    #msg = {'leftA': '200', 'rightA': '300', 'leftV': '100', 'rightV': '50'}

    print ("Waiting to receive message...")
    msg = zmq_socket.recv_json()
    print( msg )
    print( "sleeping 10" )
    time.sleep(10)
