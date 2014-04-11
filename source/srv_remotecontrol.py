import cherrypy
import zmq
import math

context = zmq.Context()
motors_socket = context.socket(zmq.PUSH)
#motors_socket = context.socket(zmq.PUB)
#motors_socket.bind("ipc:///tmp/motors.ipc") #Not supported by windows, comment out for testing
motor_socket.connect("tcp://127.0.0.2:1100")

#motors_socket.connect("tcp://localhost:8558") # Comment out for production

class RemoteControl(object):
	neutral_max = 150
	neutral_min = 105
	neutral = 128
	v_max = 100
	v_min = -100

	@cherrypy.expose
	def index(self):
		#return "ASS-Bot Remote Control Home Page<p><img src='http://10.3.1.199:8090/?action=stream' width = '720'/>"
		return "ASS-Bot Remote Control Home Page<p><img src='http://10.3.1.103:8090/?action=stream' width = '720'/>"
		# Use for web page control

	@cherrypy.expose
	def control(self, **kws):
		# if no message is received the set position to neutral, 0 acceleration
		lx = ly = rx = ry = self.neutral
		accel = 0
		
		print(kws)
		if "Mode" in kws:
			mode = str(kws['Mode'])
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

		#conversion from the arduino/ps2 controller
		#print("Checking for Arduino control...")
		if mode == "Arduino":
			print("Arduino in control")
			quad = self.which_quadrant(lx,ly)

			if quad == 1:
				rightV = self.v_max
				lfx = lx - self.neutral
				lfy = self.neutral - ly
				tmpDeg = math.degrees(math.atan2(lfy,lfx))
				leftV = (tmpDeg / 90) * self.v_max

			elif quad == 2:
				leftV = self.v_max
				lfx = self.neutral - lx
				lfy = self.neutral - ly
				tmpDeg = math.degrees(math.atan2(lfy,lfx))
				rightV = (tmpDeg / 90) * self.v_max

			elif quad == 3:
				leftV = self.v_min
				lfx = self.neutral - lx
				lfy = ly - self.neutral
				tmpDeg = math.degrees(math.atan2(lfy,lfx))
				rightV = (tmpDeg / 90) * self.v_min

			elif quad == 4:
				rightV = self.v_min
				lfx = lx - self.neutral
				lfy = ly - self.neutral
				tmpDeg = math.degrees(math.atan2(lfy,lfx))
				leftV = (tmpDeg / 90) * self.v_min

			else:  #neutral
				leftV = 0
				rightV = 0

		#leftA = rightA = accel
		leftA = rightA = 25  # 25%/s^2 change in velocity requests

		msg = {'leftA': leftA, 'rightA': rightA, 'leftV': leftV, 'rightV': rightV}
		#Send the zmq message tothe motor server
		motors_socket.send_json(msg)
		print("Message sent... leftMotor:%s rightMotor:%s" % (leftV, rightV))

		return "Received... leftH:%s leftV:%s rightH:%s rightV:%s" % (lx, ly, rx, ry)

	def which_quadrant(self, horiz, vert):
		quad = 0
		print("vert:%s  horiz:%s" % (horiz, vert))
		if ((horiz > self.neutral) and (vert < self.neutral)):
			quad = 1	# ahead right
			print("Quad 1  vert:%s  horiz:%s" % (horiz, vert))
		if ((horiz < self.neutral) and (vert < self.neutral)):
			quad = 2	# ahead left
			print("Quad 2  vert:%s  horiz:%s" % (horiz, vert))
		if ((horiz < self.neutral) and (vert > self.neutral)):
			quad = 3	# behind left
			print("Quad 3  vert:%s  horiz:%s" % (horiz, vert))
		if ((horiz > self.neutral) and (vert > self.neutral)):
			quad = 4	# behind right
			print("Quad 4  vert:%s  horiz:%s" % (horiz, vert))
		if ((horiz > self.neutral_min) and (horiz < self.neutral_max) and (vert > self.neutral_min) and (vert < self.neutral_max)):
			quad = 0	# overwrite the neutral square
			print("Quad 0  vert:%s  horiz:%s" % (horiz, vert))

		return quad

cherrypy.config.update({
    #'server.socket_host': '10.3.1.199',
    #'server.socket_host': '10.6.0.17', #uncomment for windows box testing
    'server.socket_host': '10.3.1.103',
    #'server.socket_host': '10.6.0.177',
    'server.socket_port': 8080
})

cherrypy.quickstart(RemoteControl())
