import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
from spot_status_tracker import SpotStatusUpdater
json_file_path = "spot_status.json"

class ParkingSpaceDetector:
    def __init__(self, video_path, model_path, classes_path,area_ids):
        self.cap = cv2.VideoCapture(video_path)
        self.model = YOLO(model_path)
        self.area_ids = area_ids
        self.frame_rate = 5  # Capture a frame every 1 seconds
        my_file = open(classes_path, "r")
        data = my_file.read()
        self.class_list = data.split("\n")
    def detect_objects(self, frame):
        results = self.model.predict(frame)
        boxes = results[0].boxes.data
        return pd.DataFrame(boxes).astype("float")

    def check_area(self, box, class_list):
        d=int(box[5])
        c=class_list[d]
        if 'car'in c:
            cx = int((box[0] + box[2]) / 2)
            cy = int((box[1] + box[3]) / 2)
            for area_id, area in self.area_ids.items():
                if cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False) >= 0:
                    return area_id
            return None

    def process_video(self):
        frame_count = 0
        Spots_Updater = SpotStatusUpdater(json_file_path)
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            occupied_spots = []
            frame_count += 1
            frame = cv2.resize(frame, (1280, 640))
            if frame_count % (self.frame_rate * self.cap.get(cv2.CAP_PROP_FPS)) == 0:
                boxes = self.detect_objects(frame)
                space_count = 0
                for index, row in boxes.iterrows():
                    area_id = self.check_area(row, self.class_list)
                    if area_id:
                        space_count += 1
                cv2.putText(frame, str(len(self.area_ids) - space_count), (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
                for area_id, area in self.area_ids.items():
                    if area_id in [self.check_area(row,self.class_list) for _, row in boxes.iterrows()]:
                        occupied_spots.append(area_id)
                        color = (0, 0, 255)  # Red if occupied
                    else:
                        color = (0, 255, 0)  # Green if empty
                    cv2.polylines(frame, [np.array(area, np.int32)], True, color, 2)
                Spots_Updater.update_json_status(occupied_spots)
                cv2.imshow("RGB", frame)
                time.sleep(5)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
        self.cap.release()
        cv2.destroyAllWindows()
    if __name__ == "__main__":
    # Define the main function for testing
        pass