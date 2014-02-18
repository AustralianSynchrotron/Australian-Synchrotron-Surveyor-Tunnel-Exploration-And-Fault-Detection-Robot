#!/usr/bin/env python
#

import zmq
import time
import commands

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("ipc:///tmp/motors.ipc")


while True:
   lval = input('Left speed: ')
   rval = input('Right speed: ')
   dur = input('Duration (ms): ')
   if dur > 5000:
      dur = 5000

   msg = {'leftA': '300', 'rightA': '300', 'leftV': lval, 'rightV': rval}

   print "moving for " + str(dur) + "ms"
   zmq_socket.send_json(msg)
   time.sleep(dur/1000)


   msg = {'leftA': '300', 'rightA': '300', 'leftV': '0', 'rightV': '0'}

   print "stopping"
   zmq_socket.send_json(msg)

