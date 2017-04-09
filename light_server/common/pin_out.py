import time

class PinOut:
	def __init__(self, pin_num):
		self.num = pin_num
		try:
			with open('/sys/class/gpio/export', 'w') as f:
				f.write('%s' % self.num)
		except IOError:
			pass
		with open('/sys/class/gpio/gpio%s/direction' % self.num, 'w') as f:
			f.write('out')
		self.f = open('/sys/class/gpio/gpio%s/value' % self.num, 'w')
		self.set(1)
	def set(self, val):
		self.f.write('%s' % val)
		self.f.flush()
if __name__ == '__main__':
	pin = PinOut(14)
	while 1:
		pin.set(0)
		time.sleep(delay)
		pin.set(1)
		time.sleep(delay)

