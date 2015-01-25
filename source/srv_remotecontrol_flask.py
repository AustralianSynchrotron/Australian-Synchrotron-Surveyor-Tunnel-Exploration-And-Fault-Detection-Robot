from flask import Flask, render_template
from flask.ext.socketio import SocketIO
import zmq
import math
import os
import simplejson

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)

context = zmq.Context()
motors_socket = context.socket(zmq.PUSH)
#motors_socket = context.socket(zmq.PUB)
motors_socket.connect("ipc:///tmp/motors.ipc") #Not supported by windows, comment out for testing
#motors_socket.connect("tcp://127.0.0.2:1100")
#motors_socket.connect("tcp://localhost:8558") # Comment out for production

battery_socket = context.socket(zmq.SUB)
battery_socket.connect("ipc:///tmp/battery.ipc")
battery_socket.setsockopt(zmq.SUBSCRIBE, "") #subscribe all messages

#HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html/')

class RemoteControl(object):
	neutral_max = 155
	neutral_min = 100
	neutral = 128
	v_max = 100
	v_min = -100

	@app.route('/')
	def index():
		#print HTML_DIR
		#return "ASS-Bot Remote Control Home Page<p><img src='http://10.3.1.199:8090/?action=stream' width = '720'/>"
		#return "ASS-Bot Remote Control Home Page<p><img src='http://10.3.1.103:8090/?action=stream'/>"
		#return render_template('control.html')
		# Use for web page control
		return "Testing... Testing... 1.. 2... 3...."

	@app.route('/batteries/')
	def batteries():
		msg = battery_socket.recv_json()
		print(msg)
		return msg

	@app.route('/control/')
	def control(self, **kws):
		print HTML_DIR
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

			elif quad == 5:
				leftV = self.v_min
				rightV = self.v_max

			elif quad == 6:
				leftV = self.v_max
				rightV = self.v_min

			else:  #neutral
				leftV = 0
				rightV = 0

		#leftA = rightA = accel
		leftA = rightA = 50  # 25%/s^2 change in velocity requests

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
		if ((horiz < 20) and (vert > 115) and (vert < 140)):
			quad = 5
			print("Spin Left!")
		if ((horiz > 230) and (vert > 115) and (vert <140)):
			quad = 6
			print("Spin Right!")
		if ((horiz > self.neutral_min) and (horiz < self.neutral_max) and (vert > self.neutral_min) and (vert < self.neutral_max)):
			quad = 0	# overwrite the neutral square
			print("Quad 0  vert:%s  horiz:%s" % (horiz, vert))

		return quad

if __name__ == '__main__':
    socketio.run(app,port=8081)
