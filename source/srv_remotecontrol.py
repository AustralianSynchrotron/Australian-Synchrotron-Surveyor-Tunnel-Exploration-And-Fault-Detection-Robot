import cherrypy
import zmq
import math

context = zmq.Context()
#motors_socket = context.socket(zmq.PUSH)
motors_socket = context.socket(zmq.PUB)
motors_socket.bind("ipc:///tmp/motors.ipc") #Not supported by windows, comment out for testing
#motors_socket.connect("tcp://localhost:8558") # Comment out for production

class RemoteControl(object):
	neutral_max = 137
	neutral_min = 118
	neutral = 128
	v_max = 100
	v_min = -100

	@cherrypy.expose
	def index(self):
		#return "ASS-Bot Remote Control Home Page<p><img src='http://10.3.1.199:8090/?action=stream' width = '720'/>"
		return "ASS-Bot Remote Control Home Page<p><img src='http://10.3.1.83:8090/?action=stream' width = '720'/>"
		# Use for web page control

	@cherrypy.expose
	def control(self, **kws):
		# if no message is received the set position to neutral, 0 acceleration
		lx = ly = rx = ry = self.neutral
		accel = 0
		
		print(kws)

		if "Lx" in kws:
			lx = int(kws['Lx'])
		if "Ly" in kws:
			ly = int(kws['Ly'])
		if "Rx" in kws:
			rx = int(kws['Rx'])
		if "Ry" in kws:
			ry = int(kws['Ry'])
		if "BtnX" in kws:
			accel = int(kws['BtnX'])
		if "Sel" in kws:
			sel = int(kws['Sel'])

		print("Received... leftH:%s leftV:%s rightH:%s rightV:%s speed:%s" % (lx, ly, rx, ry, accel))

		# Left stick controls vehicle base movement
		# Right stick auxilary device control
		# - use select button to change between devices
		# X Button (blue) motor acceleration / enable movement
		# dead band around neutral analog stick position +/-10units

		#convert coordinate system 0 - 128
		#convert to a number between 0 and 100 or 0 and -100 for reverse.

		quad = self.which_quadrant(lx,ly)

		if quad == 1:
			leftV = self.v_max
			lfx = lx - self.neutral
			lfy = self.neutral - ly
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			rightV = (tmpDeg / 90) * self.v_max

		elif quad == 2:
			rightV = self.v_max
			lfx = self.neutral - lx
			lfy = self.neutral - ly
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			leftV = (tmpDeg / 90) * self.v_max

		elif quad == 3:
			rightV = self.v_min
			lfx = self.neutral - lx
			lfy = ly - self.neutral
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			leftV = (tmpDeg / 90) * self.v_min

		elif quad == 4:
			leftV = self.v_min
			lfx = lx - self.neutral
			lfy = ly - self.neutral
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			rightV = (tmpDeg / 90) * self.v_min

		else:  #neutral
			leftV = 0
			rightV = 0

		leftA = rightA = accel

		msg = {'leftA': leftA, 'rightA': rightA, 'leftV': leftV, 'rightV': rightV}
		#Send the zmq message tothe motor server
		motors_socket.send_json(msg)

		return "Received... leftH:%s leftV:%s rightH:%s rightV:%s" % (lx, ly, rx, ry)

	def which_quadrant(self, horiz, vert):
		quad = 0
		if ((horiz > self.neutral_max) and (vert < self.neutral_min)):
			quad = 1
		if ((horiz < self.neutral_min) and (vert < self.neutral_min)):
			quad = 2
		if ((horiz < self.neutral_min) and (vert > self.neutral_max)):
			quad = 3
		if ((horiz > self.neutral_max) and (vert > self.neutral_max)):
			quad = 4

		return quad

cherrypy.config.update({
    #'server.socket_host': '10.3.1.199',
    #'server.socket_host': '10.6.0.17', #uncomment for windows box testing
    'server.socket_host': '10.3.1.83',
    'server.socket_port': 8080
})

cherrypy.quickstart(RemoteControl())
