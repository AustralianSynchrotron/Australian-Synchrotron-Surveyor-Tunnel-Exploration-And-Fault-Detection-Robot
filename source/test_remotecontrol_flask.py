from gevent import monkey
monkey.patch_all()
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room

import zmq

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
def background_thread():
    context = zmq.Context()
    battery_socket = context.socket(zmq.SUB)
    battery_socket.connect("ipc:///tmp/battery.ipc")
    battery_socket.setsockopt(zmq.SUBSCRIBE, '') #subscribe to all messages

    bumper_socket = context.socket(zmq.SUB)
    bumper_socket.connect("ipc:///tmp/bumper.ipc")
    bumper_socket.setsockopt(zmq.SUBSCRIBE, '') #subscribe to all messages

    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
            {'data': 'Server generated event', 'count': count},
            namespace='')

        msg = battery_socket.recv_json()
        print('Message Recieved: %s' % msg )
        socketio.emit('battery response',
            {'data': msg},
            namespace='')

        bmp = bumper_socket.recv_json()
        print('Message Recieved: %s' % bmp )
        socketio.emit('bumper response',
            {'data': bmp},
            namespace='')

@app.route('/')
def index():
    global thread
    #if thread is None:
    if not thread.isAlive():
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')

@socketio.on('update_battery', namespace='')
def update_battery(message):
    emit('battery response',
        {'data': message['data']})
    print message['data']

@socketio.on('update_bumper', namespace='')
def update_bumper(message):
    emit('bumper response',
        {'data': message['data']})
    print message['data']

@socketio.on('my event', namespace='')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        {'data': message['data'], 'count': session['receive_count']})

@socketio.on('my broadcast event', namespace='')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        {'data': message['data'], 'count': session['receive_count']},
        broadcast=True)

@socketio.on('join', namespace='')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
        'count': session['receive_count']})

@socketio.on('leave', namespace='')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
        'count': session['receive_count']})

@socketio.on('my room event', namespace='')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        {'data': message['data'], 'count': session['receive_count']},
        room=message['room'])

@socketio.on('connect', namespace='')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app,port=8002,host="10.3.2.76")
