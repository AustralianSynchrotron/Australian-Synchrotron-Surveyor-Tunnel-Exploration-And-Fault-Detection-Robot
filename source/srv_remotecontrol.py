import cherrypy

class RemoteControl(object):
	@cherrypy.expose
	def index(self):
		return "Home PAge"

	@cherrypy.expose
	def control(self, **kws):

		lx = kws['Lx']
		ly = kws['Ly']

		rx = kws['Rx']
		ry = kws['Ry']

		print("Received... leftH:%s leftV:%s rightH:%s rightV%s" % lx, ly, rx, ry)

		return "Received... leftH:%s leftV:%s rightH:%s rightV%s" % lx, ly, rx, ry

cherrypy.config.update({
    #'server.socket_host': '10.6.100.199',
    'server.socket_port': 80
})

cherrypy.quickstart(RemoteControl())