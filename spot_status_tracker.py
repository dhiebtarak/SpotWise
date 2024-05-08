import json
from datetime import datetime

class SpotStatusUpdater:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.changes_file_path = ""  # New JSON file for changes

    def update_json_status(self, occupied_spots):
        # Load the JSON data
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)
            camera_id = data.get("camera_id", "")  # Extract camera ID from JSON data
            self.changes_file_path = f"spot_changes_{camera_id}.json"
        # Update the status and timestamp of the provided spots
        changes = []  # List to store changes

        for spot in data['parking_space']:
            spot["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if spot['spot_id'] in occupied_spots:
                if spot['status'] != 'occupied':  # Check if status changed
                    spot['status'] = 'occupied'
                    changes.append({"floor":data["floor"],'spot_id': spot['spot_id'], 'status': 'occupied'})
            else:
                if spot['status'] != 'empty':  # Check if status changed
                    spot['status'] = 'empty'
                    changes.append({"floor":data["floor"],'spot_id': spot['spot_id'], 'status': 'empty'})

        # Write the updated data back to the original JSON file
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        if changes:
            with open(self.changes_file_path, 'w') as changes_file:
                json.dump(changes, changes_file)
        if not changes:
            with open(self.changes_file_path, 'w') as changes_file:
                changes_file.write('{}')