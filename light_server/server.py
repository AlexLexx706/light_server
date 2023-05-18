from gevent.pywsgi import WSGIServer
from flask import Flask, request, json
from flask import render_template
from light_server.common import pin_out

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
pins = {
    0: pin_out.PinOut(14),
    1: pin_out.PinOut(15)}
COUNTER = 0


@app.route("/")
def hello():
    """provide main page

    Returns:
        string: html page
    """
    return render_template('hello.html', counter=COUNTER)


@app.route('/api/light', methods=['PUT'])
def light():
    """change GPIO state
    Returns:
        string: json string with result of changing ping state
    """
    data = request.get_json()
    try:
        pins[data['id']].set(data['value'])
        return json.dumps({'res': "ok"})
    except KeyError:
        json.dumps({'res': f"wrong light id:{data['id']}"})


def main():
    """Server
    """
    port = 8080
    print("start server on port:{port}")
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
