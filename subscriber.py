import paho.mqtt.client as mqtt

# Define MQTT settings
broker_address = "127.0.0.1"  # Public MQTT broker for testing purposes
port = 1883
topic = "spot_changes"

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, port, 60)

try:
    # Start the MQTT loop to receive messages
    client.loop_forever()
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully terminate the script
    print("Script terminated by user")
    client.disconnect()
    client.loop_stop()
