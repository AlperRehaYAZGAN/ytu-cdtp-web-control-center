#./venv/Scripts/python.exe

# YTU CDTP - Raspberry Pi Camera Streaming Server PC Proxy Camera Streaming
# Author: Alper Reha YAZGAN
# Date: 08.12.2021

#
#   APP INTERNAL DEPENDENCIES
#
from os import getcwd,getenv
import json
import time
import cv2
# dotenv
from dotenv import load_dotenv
load_dotenv(dotenv_path= getcwd() + '/' + '.env')

# dotenv initial values
PI_STREAM_HOST = getenv("PI_STREAM_HOST", "localhost")
PI_STREAM_PORT = int(getenv("PI_STREAM_PORT", "5000"))
PI_STREAM_URL = getenv("PI_STREAM_URL","/video_feed")
PI_CAMERA_PORT = int(getenv('PI_CAMERA_PORT',0))

# print env vars
print("PI_STREAM_HOST:", PI_STREAM_HOST)
print("PI_STREAM_PORT:", PI_STREAM_PORT)
print("PI_STREAM_URL:", PI_STREAM_URL)
print("PI_CAMERA_PORT:", PI_CAMERA_PORT)

# docs: https://stackoverflow.com/questions/55651836/how-can-i-fetch-live-stream-from-url
opencv_catcher = cv2.VideoCapture("http://localhost:5001/video_feed") 


def main():
    while True:
        try:
            # Display frames in main program
            if opencv_catcher.isOpened():
                status, frame = opencv_catcher.read()
                # Press Q on keyboard to stop recording
                cv2.imshow('OpenCV Catcher', frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyAllWindows()
                exit(1)
        except AttributeError:
            cv2.destroyAllWindows()
            exit(1)
            pass


if __name__ == '__main__':
    main()






