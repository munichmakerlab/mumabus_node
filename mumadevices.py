class MuMaBusDevice:
	def __init__(self, name):
		self._name = name
	
	def action(self, topic, payload):
		pass

class SwitchDevice(MuMaBusDevice):
	def __init__(self, name, board, pin):
		MuMaBusNode.__init__(self, name)
		
		self._board = board
		self._pin_no = pin
		self._pin = board.get_pin('d:' + str(pin)+ ':o')
		
		self._state = 0
		self._pin.write(0)
	
	def action(self, topic, payload):
		if topic == "/state":
			if payload == 0:
				self._state = 0
				self._ping.write(0)
			elif payload == 1:
				self._state = 0
				self._ping.write(0)
