from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template, request, json, redirect, url_for, session
from flask_socketio import SocketIO, send, emit

import logging

from relay.relay import RelayMonitor

relays = [{"ip":"192.168.4.116", "worker": None}]

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'secret!' # НУ мего секрет, испольщуеться для шафрования данных сесии
app.config["DEBUG"] = True
app.connecions_n = 0

socketio = SocketIO(app)

# CONTROL pins!!!
pins = {
    0: 0,
    1: 1,
    2: 1,
    3: 0,
    4: 0,
    5: 1,
}

# acces to user!!! Ну суппер секрет!!!, используеться для логина 
user = {
    'username': 'admin',
    'password': '123456'
}

def start_relay_workers():
    for r in relays:
        if r['worker'] is None:
            r['worker']  = RelayMonitor(r['ip'])
            r['worker'].start()


def stop_relay_workers():
    for r in relays:
        if r['worker'] is not None:
            r['worker'].stop()
            r['worker'] = None

@socketio.on('connect')
def connect():
    app.connecions_n += 1
    app.logger.info(f'connect: clients {app.connecions_n}')


@socketio.on('disconnect')
def disconnect():
    app.connecions_n -= 1
    if app.connecions_n == 0:
        stop_relay_workers()
    app.logger.info(f'disconnect: clients {app.connecions_n}')


@socketio.on('value_changed')
def handle_value_changed(data):
    """hendler for client data
    Args:
        data (json): client data:{'id':int, 'value':0/1}
    """
    app.logger.info('received json: %s', str(data))
    pins[data['id']] = data['value']
    emit('update_value', data, broadcast=True)


@app.route('/')
def index():
    """handle first page, reducrect to login
    """
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """login handle"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user['username'] == username and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    """logout handler"""
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/dashboard")
def dashboard():
    """provide main working

    Returns:
        string: html page
    """
    # authorization check, if there is no authorization, go to the login page
    if 'username' not in session:
        return redirect(url_for('login'))

    app.logger.info('dashboard, user:%s', session["username"])
    
    # normal workflow
    start_relay_workers()
            
    buttons = [
        {'name':'AGI2 rev6.10', 'power': {'id':0, 'value':pins[0]}, 'timer': {'id':1, 'value':pins[1]}},
        {'name':'AGI2 rev9.17', 'power':{'id':2, 'value':pins[2]}, 'timer': {'id':3, 'value':pins[3]}},
        {'name':'AGVL','power': {'id':4, 'value':pins[4]}, 'timer': {'id':5, 'value':pins[5]}}
]   
    app.logger.info('hello: %s', buttons)
    return render_template(
        'dashboard.html',
        buttons=buttons)


def main():
    """
        Server
    """
    port = 7079
    socketio.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
