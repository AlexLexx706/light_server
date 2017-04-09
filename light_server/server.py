from common import pin_out
from gevent.wsgi import WSGIServer
from flask import Flask, request, json
from flask import render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
pins ={
	0: pin_out.PinOut(14),
	1: pin_out.PinOut(15)}
counter = 0

@app.route("/")
def hello():
   global counter
   return render_template('hello.html', counter=counter)

@app.route('/api/light', methods=['PUT'])
def light():
	data = request.get_json()
	try:
		pins[data['id']].set(data['value'])
		return json.dumps({'res':"ok"})
	except 	KeyError:
		json.dumps({'res':'wrong light id:%s' % data['id']})

if __name__ == '__main__':
   http_server = WSGIServer(('', 8080), app)
   http_server.serve_forever()
