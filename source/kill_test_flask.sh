ps axf | grep test_remotecontrol_flask.py | grep -v grep | awk '{print "kill -9 " $1}' | sh 
