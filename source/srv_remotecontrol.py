import cherrypy
import zmq

context = zmq.Context()
motors_socket = context.socket(zmq.PUSH)
#motors_socket.bind("ipc:///tmp/motors.ipc") #Not supported by windows, comment out for testing
motors_socket.connect("tcp://localhost:8558") # Comment out for production

class RemoteControl(object):
	@cherrypy.expose
	def index(self):
		return "ASS-Bot Remote Control Home Page"

	@cherrypy.expose
	def control(self, **kws):
		# if no message is received the set position to neutral
		lx = 128
		ly = 128
		rx = 128
		ry = 128

		print(kws)

		if "Lx" in kws:
			lx = kws['Lx']
		if "Ly" in kws:
			ly = kws['Ly']
		if "Rx" in kws:
			rx = kws['Rx']
		if "Ry" in kws:
			ry = kws['Ry']
		if "BtnX" in kws:
			accel = kws['BtnX']

		print("Received... leftH:%s leftV:%s rightH:%s rightV:%s speed:%s" % (lx, ly, rx, ry, accel))

		return "Received... leftH:%s leftV:%s rightH:%s rightV:%s" % (lx, ly, rx, ry)

cherrypy.config.update({
    #'server.socket_host': '10.6.100.199',
    'server.socket_host': '10.6.0.17', #uncomment for windows box testing
    'server.socket_port': 8080
})

cherrypy.quickstart(RemoteControl())