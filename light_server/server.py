from flask import Flask, request, json
from flask import render_template
from flask_socketio import SocketIO, send, emit
from light_server.common import pin_out
import logging

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'secret!'
app.config["DEBUG"] = True
clients_counter = 0
socketio = SocketIO(app)

# CONTROL pins!!!
pins = {
    0: pin_out.PinOut(14, 'Timer enable'),
    1: pin_out.PinOut(15, 'Power'),
    2: pin_out.PinOut(14, 'Timer enable AGI2 rev6.11'),
    3: pin_out.PinOut(15, 'Power AGI2 rev6.11'),
    4: pin_out.PinOut(14, 'Timer enable, хз что'),
    5: pin_out.PinOut(15, 'Power, хз что'),
}

@socketio.on('value_changed')
def handle_value_changed(data):
    """hendler for client data
    Args:
        data (json): client data:{'id':int, 'value':0/1}
    """
    app.logger.info('received json: %s', str(data))
    pins[data['id']].set(data['value'])
    emit('update_value', data, broadcast=True)


@socketio.event
def connect(**args):
    global clients_counter
    clients_counter += 1
    print(f'connect clients_counter:{clients_counter} args:{args}')

@socketio.event
def disconnect(**args):
    global clients_counter
    clients_counter -= 1
    print(f'disconnect clients_counter:{clients_counter} args:{args}')


@app.route("/")
def hello():
    """provide main page

    Returns:
        string: html page
    """
    buttons = [{'id': key, 'value': pin.value, 'name': pin.name}
               for key, pin in pins.items()]
    app.logger.info('hello: %s', buttons)

    return render_template(
        'hello.html',
        buttons=buttons)


def main():
    """Server
    """
    port = 8080
    socketio.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
