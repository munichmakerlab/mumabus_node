from pyfirmata import Arduino, util
import mosquitto
from mumadevices import *

import config

def on_message(mosq, obj, msg):
	# remove prefix from topic.
	if msg.topic.startswith(config.topic_prefix):
		node = msg.topic[len(config.topic_prefix):]
	else:
		return
	node, topic = node.split('/', 1)
	
	items[node].action(topic, msg.payload)

board = Arduino(config.arduino_port)

# initialize MQTT
mqtt_client = mosquitto.Mosquitto(config.node_name)
mqtt_client.username_pw_set(config.broker["user"], config.broker["password"])
mqtt_client.on_message = on_message
mqtt_client.connect(config.broker["hostname"], config.broker["port"], 60)

items = {}

for (name, details) in config.devices.items():
	item = {}
	if details["type"] == "switch":
		if len(details["pins"]) != 1:
			print "Device \"" + name + "\" is invalid."
			continue
		item = SwitchDevice(name, board, details["pins"][0])
		mqtt_client.subscribe(config.topic_prefix + name + "/#", 1)
	items.append(item)

# Enable relais board
board.digital[6].write(1)

mqtt_client.loop_forever()
