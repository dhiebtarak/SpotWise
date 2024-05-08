from video_click_processor import SpotsDetector
video_processor = SpotsDetector(r"C:\Users\21629\Desktop\camera\Cameras\cam6.mp4")
video_processor.process_video()
formatted_clicks = video_processor.get_formatted_clicks()
print("Mouse Click Positions:", formatted_clicks)