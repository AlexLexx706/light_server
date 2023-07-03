from gevent import monkey; monkey.patch_all()
from flask import Flask, request, json
from flask import render_template
from flask_socketio import SocketIO, send, emit
import logging

from relay.relay import RelayMonitor

relays = [{"ip":"192.168.4.116", "worker": None}]

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'secret!'
app.config["DEBUG"] = True

socketio = SocketIO(app)
connecions_n = 0

# CONTROL pins!!!
pins = {
    0: 0,
    1: 1,
    2: 1,
    3: 0,
    4: 0,
    5: 1,
}

def start_relay_workers():
    app.logger.info('start_relay_workers 1.')
    for r in relays:
        app.logger.info('start_relay_workers 2.')
        if r['worker'] is None:
            app.logger.info('start_relay_workers 3.')
            r['worker']  = RelayMonitor(r['ip'])
            app.logger.info('start_relay_workers 4.')
            r['worker'].start()
            app.logger.info(f'START relay {r["ip"]}')


def stop_relay_workers():
    app.logger.info('stop_relay_workers 1.')
    for r in relays:
        app.logger.info('stop_relay_workers 2.')
        if r['worker'] is not None:
            app.logger.info('stop_relay_workers 3.')
            r['worker'].stop()
            app.logger.info('stop_relay_workers 4.')
            r['worker'] = None
            app.logger.info(f'STOP relay {r["ip"]}')

@socketio.on('connect')
def connect():
    global connecions_n
    connecions_n+= 1
    app.logger.info(f'connect: clients {connecions_n}')


@socketio.on('disconnect')
def disconnect():
    global connecions_n
    connecions_n-= 1
    if connecions_n == 0:
        stop_relay_workers()
    app.logger.info(f'disconnect: clients {connecions_n}')


@socketio.on('value_changed')
def handle_value_changed(data):
    """hendler for client data
    Args:
        data (json): client data:{'id':int, 'value':0/1}
    """
    app.logger.info('received json: %s', str(data))
    pins[data['id']] = data['value']
    emit('update_value', data, broadcast=True)



@app.route("/")
def hello():
    """provide main page

    Returns:
        string: html page
    """
    app.logger.info('hello 1.')
    start_relay_workers()
    app.logger.info('hello 2.')
            
    buttons = [
        {'name':'AGI2 rev6.10', 'power': {'id':0, 'value':pins[0]}, 'timer': {'id':1, 'value':pins[1]}},
        {'name':'AGI2 rev9.17', 'power':{'id':2, 'value':pins[2]}, 'timer': {'id':3, 'value':pins[3]}},
        {'name':'AGVL','power': {'id':4, 'value':pins[4]}, 'timer': {'id':5, 'value':pins[5]}}
]   
    app.logger.info('hello: %s', buttons)
    return render_template(
        'hello.html',
        buttons=buttons)


def main():
    """
        Server
    """
    port = 7078
    socketio.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
