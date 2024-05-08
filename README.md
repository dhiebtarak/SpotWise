# SpotWise
Your parking assistance
Searching for available parking spaces is often tedious, stressful and contributes to traffic jams. Additionally, locating your vehicle in a sprawling parking lot can present a considerable challenge. The objective of this project is to develop “SpotWise”, a system designed to assist drivers with parking, with a specific focus on shopping centers. SpotWise leverages computer vision and IoT technologies to solve these persistent problems. Through the implementation of advanced parking spot detection and monitoring, efficient path finding, as well as a mobile app, SpotWise simplifies the parking experience, reducing driver stress and optimizing the use of available parking spaces.

## Requirements
- Python 3.11.5 installed on your system.
- Jupyter Notebook installed (optional but recommended).

## To run the project, follow these steps:

1  Open a command prompt.
2  Navigate to the directory containing the project files.
3  Run the command python main.py.
4  The main.py script will execute, which in turn will run the multitask, publisher, and subscriber processes.

## Interacting with the Scripts

The publisher.py script will publish messages to the MQTT broker.
The subscriber.py script will subscribe to topics on the MQTT broker and receive messages.
The multitask.py script will demonstrate running multiple tasks concurrently.