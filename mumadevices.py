import subprocess
import config

class MuMaBusDevice:
	def __init__(self, name):
		self._name = name
	
	def action(self, topic, payload):
		pass

class SwitchDevice(MuMaBusDevice):
	def __init__(self, name, board, pin):
		MuMaBusDevice.__init__(self, name)
		
		self._board = board
		self._pin_no = pin
		self._pin = board.get_pin('d:' + str(pin)+ ':o')
		
		self._state = 0
		self._pin.write(1)
	
	def action(self, topic, payload):
		if topic == "state":
			if payload == "0":
				self._state = 0
				self._pin.write(1)
				print "turned off"
			elif payload == "1":
				self._state = 0
				self._pin.write(0)
				print "turned on"
			else:
				print "invalid payload"
			
class RCSwitchDevice(MuMaBusDevice):
	def __init__(self, name, address):
		MuMaBusDevice.__init__(self, name)
		
		self._address = address
		self._state = -1
	
	def action(self, topic, payload):
		if topic == "state":
			if payload == "0":
				self._state = 1
				
				params = [ "sudo", config.rcswitch_path ]
				params.extend(self._address)
				params.append("0")
				
				subprocess.call(params)
				print "turned off"
			elif payload == "1":
				self._state = 1
				
				params = [ "sudo", config.rcswitch_path ]
				params.extend(self._address)
				params.append("1")
				
				subprocess.call(params)
			else:
				print "invalid payload"
