import paho.mqtt.client as mqtt
import json
import time
import os

# Define MQTT settings
broker_address = "127.0.0.1"  # MQTT broker address
port = 1883
topic = "spot_changes"  # MQTT topic for publishing changes

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

def on_publish(client, userdata, mid):
    print("Message published")

def is_file_empty(file_path):
    return os.stat(file_path).st_size == 2

# Function to publish changes from JSON file
def publish_changes(client):
    if not is_file_empty("spot_changes.json"):
        with open("spot_changes.json", 'r') as changes_file:
            changes_data = changes_file.read()
        client.publish(topic, json.dumps(changes_data))

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.on_publish = on_publish

# Connect to MQTT broker
client.connect(broker_address, port, 60)
try:
# Main loop to continuously monitor changes and publish data
    while True:
        # Check for changes in the JSON file and publish if there are any
        
        publish_changes(client)
        
        # Sleep for a short duration before checking again (adjust as needed)
        time.sleep(5)
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully terminate the script
    print("Script terminated by user")
    client.disconnect()
    client.loop_stop()