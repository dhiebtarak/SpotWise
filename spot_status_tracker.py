import json
from datetime import datetime

class SpotStatusUpdater:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def update_json_status(self, occupied_spots):
        # Load the JSON data
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Update the status and timestamp of the provided spots
        current_date = datetime.now().isoformat()
        for spot in data['parking_space']:
            if spot['spot_id'] in occupied_spots:
                spot['status'] = 'occupied'
            else:
                spot['status'] = 'empty'
            spot['timestamp'] = current_date

        # Write the updated data back to the JSON file
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)