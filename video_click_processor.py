import cv2
import time
class SpotsDetector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.clicks = []
        self.cap = cv2.VideoCapture(self.video_path)
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicks.append((x, y))

    def process_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("End of video")
                break

            frame = cv2.resize(frame, (1280, 640))
            cv2.imshow('frame', frame)
            time.sleep(1)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_formatted_clicks(self):
        formatted_clicks = '[' + ','.join([f'({x},{y})' for x, y in self.clicks]) + ']'
        return formatted_clicks