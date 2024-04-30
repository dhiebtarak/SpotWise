import json
from datetime import datetime

class SpotStatusUpdater:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.changes_file_path = "spot_changes.json"  # New JSON file for changes

    def update_json_status(self, occupied_spots):
        # Load the JSON data
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Update the status and timestamp of the provided spots
        current_date = datetime.now().isoformat()
        changes = []  # List to store changes

        for spot in data['parking_space']:
            if spot['spot_id'] in occupied_spots:
                if spot['status'] != 'occupied':  # Check if status changed
                    spot['status'] = 'occupied'
                    spot['timestamp'] = current_date
                    changes.append({'spot_id': spot['spot_id'], 'status': 'occupied', 'timestamp': current_date})
            else:
                if spot['status'] != 'empty':  # Check if status changed
                    spot['status'] = 'empty'
                    spot['timestamp'] = current_date
                    changes.append({'spot_id': spot['spot_id'], 'status': 'empty', 'timestamp': current_date})

        # Write the updated data back to the original JSON file
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        if changes:
            with open(self.changes_file_path, 'w') as changes_file:
                json.dump(changes, changes_file)
        if not changes:
            with open(self.changes_file_path, 'w') as changes_file:
                changes_file.write('{}')