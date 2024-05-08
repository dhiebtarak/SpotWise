import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
from spot_status_tracker import SpotStatusUpdater
import asyncify
import asyncio

class ParkingSpaceDetector:
    def __init__(self, video_path, json_file_path, model_path, classes_path,area_ids, show = True):
        self.cap = cv2.VideoCapture(video_path)
        self.model = YOLO(model_path)
        self.json_file_path = json_file_path
        self.area_ids = area_ids
        self.frame_rate = 5  # Capture a frame every 1 seconds
        my_file = open(classes_path, "r")
        data = my_file.read()
        self.class_list = data.split("\n")
        self.show = show

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

    async def process_video(self):
        frame_count = 0
        Spots_Updater = SpotStatusUpdater(self.json_file_path)
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            occupied_spots = []
            frame_count += 1
            frame = cv2.resize(frame, (1280, 640))
            if frame_count % (self.frame_rate * self.cap.get(cv2.CAP_PROP_FPS)) == 0:
                boxes = self.detect_objects(frame)
                for index, row in boxes.iterrows():
                    area_id = self.check_area(row, self.class_list)
                for area_id, area in self.area_ids.items():
                    if area_id in [self.check_area(row,self.class_list) for _, row in boxes.iterrows()]:
                        occupied_spots.append(area_id)
                Spots_Updater.update_json_status(occupied_spots)
                #if self.show:
                    #cv2.imshow("RGB", frame)
                await asyncio.sleep(5)  # Use await inside async function

    def run(self):  # Define a run method to start the async function
        asyncio.run(self.process_video())


if __name__ == "__main__":
    # Define the main function for testing
    pass