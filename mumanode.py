import paho.mqtt.client as paho
from mumadevices import *
from threading import Timer
import logging

import config


def on_connect(mosq, obj, rc):
	logging.info("Connect with RC " + str(rc))

def on_message(mosq, obj, msg):
	logging.info(msg.topic + " [" + str(msg.qos) + "]: " + str(msg.payload))
	# remove prefix from topic.
	if msg.topic.startswith(config.topic_prefix):
		node = msg.topic[len(config.topic_prefix):]
	else:
		return
	node, topic = node.split('/', 1)
	items[node].action(topic, msg.payload)


def on_subscribe(mosq, obj, mid, granted_qos):
	logging.info("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_disconnect(client, userdata, rc):
	logging.warning("Disconnected (RC " + str(rc) + ")")
	if rc <> 0:
		try_reconnect(client)

def on_log(client, userdata, level, buf):
	logging.debug(buf)
	
def try_reconnect(client, time = 60):
	try:
		logging.info("Trying reconnect")
		client.reconnect()
	except:
		logging.warning("Reconnect failed. Trying again in " + str(time) + " seconds")
		Timer(time, try_reconnect, [client]).start()

logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

logging.info("Initializing MQTT")
mqttc = paho.Client(config.node_name)
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
try:
	mqttc.connect(config.broker["hostname"], config.broker["port"])
except:
	logging.warning("Connection failed. Trying again in 30 seconds")
	Timer(30, try_reconnect, [mqttc]).start()

items = {}

for (name, details) in config.devices.items():
	item = {}
	if details["type"] == "switch":
		if len(details["pins"]) != 1:
			logging.error("Device \"" + name + "\" is invalid.")
			continue
		item = SwitchDevice(name, board, details["pins"][0])
		mqttc.subscribe(config.topic_prefix + name + "/#", 1)
	elif details["type"] == "rcswitch":
		item = RCSwitchDevice(name, details["address"])
		mqttc.subscribe(config.topic_prefix + name + "/#", 1)
	items[name] = (item)
	logging.info("Added device " + name)

logging.info("Entering loop")
try:
	mqttc.loop_forever()
except KeyboardInterrupt:
	pass

logging.info("Exiting")
mqttc.disconnect()
