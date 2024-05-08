import paho.mqtt.client as mqtt
import json
import time
import os
broker_address = "127.0.0.1"  # MQTT broker address
port = 1883
topics = ["spot_changes1", "spot_changes2", "spot_changes3", "spot_changes4", "spot_changes5", "spot_changes6"]

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for topic in topics:
        client.subscribe(topic)

def on_publish(client, userdata, mid):
    print("Message published")

def is_file_empty(file_path):
    return os.stat(file_path).st_size == 2


# Function to publish changes from JSON file
def publish_changes(client, topic):
    topic_index = topics.index(topic) + 1
    json_file_path = f"spot_changes_cam{topic_index}.json"
    
    # Load current changes data from file
    if not is_file_empty(json_file_path):
        with open(json_file_path, 'r') as changes_file:
            current_changes_data = changes_file.read()
    else:
        current_changes_data = {}
    
    # Load previously published changes data, if available
    previous_changes_data = client.previous_changes.get(topic)
    # Check if current and previous data are different
    if current_changes_data != previous_changes_data:
        if  str(current_changes_data)!="{}":
            client.publish(topic, json.dumps(current_changes_data))
        
        # Update the previous_changes dictionary with the current data
    client.previous_changes[topic] = current_changes_data

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.previous_changes = {}
# Connect to MQTT broker
client.connect(broker_address, port, 60)

try:
    # Main loop to continuously monitor changes and publish data
    while True:
        # Check for changes in the JSON file and publish if there are any
        for topic in topics:
            publish_changes(client, topic)
        
        # Sleep for a short duration before checking again (adjust as needed)
        time.sleep(5)
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully terminate the script
    print("Script terminated by user")
    client.disconnect()