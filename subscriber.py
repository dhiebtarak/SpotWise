import paho.mqtt.client as mqtt
import json 
import requests

# Define URL for POST requests
url = "http://localhost:8000/data1"

# Define MQTT settings
broker_address = "127.0.0.1"  # Public MQTT broker for testing purposes
port = 1883
topics = ["spot_changes1", "spot_changes2", "spot_changes3", 
          "spot_changes4", "spot_changes5", "spot_changes6"]

# MQTT callback for message reception
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to all topics
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    try:
        # Parse the JSON message
        data = msg.payload.decode() 
        data = json.loads(data)
        data = data[1:-1]
        data = json.loads(data) 
        
        # Extract topic from message
        topic = msg.topic

        # Send data to URL based on topic
        response = requests.post(url, json=data)
     
        print("Data to be sent:", data)  # Debugging statement
        print("Response:", response.status_code)  # Debugging statement
        print("Response Content:", response.text)  # Debugging statement
    except Exception as e:
        print("Error:", e)

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