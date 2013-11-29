import cherrypy

class RemoteControl(object):
	@cherrypy.expose
	def index(self):
		return "Home PAge"

	@cherrypy.expose
	def control(self, **kws):
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

		print("Received... leftH:%s leftV:%s rightH:%s rightV:%s" % (lx, ly, rx, ry))

		return "Received... leftH:%s leftV:%s rightH:%s rightV:%s" % (lx, ly, rx, ry)

cherrypy.config.update({
    #'server.socket_host': '10.6.100.199',
    'server.socket_host': '10.6.0.17',
    'server.socket_port': 8080
})

cherrypy.quickstart(RemoteControl())