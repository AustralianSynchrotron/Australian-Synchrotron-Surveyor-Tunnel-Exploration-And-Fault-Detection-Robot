import cherrypy
import zmq
import math

context = zmq.Context()
motors_socket = context.socket(zmq.PUSH)
#motors_socket.bind("ipc:///tmp/motors.ipc") #Not supported by windows, comment out for testing
motors_socket.connect("tcp://localhost:8558") # Comment out for production

class RemoteControl(object):
	neutral_max = 137
	neutral_min = 118
	v_max = 100
	v_min = -100

	@cherrypy.expose
	def index(self):
		return "ASS-Bot Remote Control Home Page"
		# Use for web page control

	@cherrypy.expose
	def control(self, **kws):
		# if no message is received the set position to neutral
		lx = 128
		ly = 128
		rx = 128
		ry = 128

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
			leftV = 100
			lfx = lx - 128
			lfy = 128 - ly
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			rightV = (tmpDeg / 90) * 100

		elif quad == 2:
			rightV = 100
			lfx = 128 - lx
			lfy = 128 - ly
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			leftV = (tmpDeg / 90) * 100

		elif quad == 3:
			rightV = -100
			lfx = 128 - lx
			lfy = ly - 128
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			leftV = -(tmpDeg / 90) * 100

		elif quad == 4:
			leftV = -100
			lfx = lx - 128
			lfy = ly - 128
			tmpDeg = math.degrees(math.atan2(lfy,lfx))
			rightV = -(tmpDeg / 90) * 100

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
    #'server.socket_host': '10.6.100.199',
    'server.socket_host': '10.6.0.17', #uncomment for windows box testing
    'server.socket_port': 8080
})

cherrypy.quickstart(RemoteControl())