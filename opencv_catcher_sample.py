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

# docs: https://stackoverflow.com/questions/55651836/how-can-i-fetch-live-stream-from-url
CV2_STREAM_FROM_1 = getenv("CV2_STREAM_FROM_1",0)
# check if CV2_STREAM_FROM_1 is a valid camera port
if CV2_STREAM_FROM_1.isdigit():
    # cast to int
    CV2_STREAM_FROM_1 = int(CV2_STREAM_FROM_1)
# print CV2_STREAM_FROM_2
print("CV2_STREAM_FROM_1:", CV2_STREAM_FROM_1)
opencv_catcher = cv2.VideoCapture(CV2_STREAM_FROM_1,cv2.CAP_DSHOW) 
opencv_catcher.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
opencv_catcher.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)


def main():
    while True:
        try:
            # Display frames in main program
            if opencv_catcher.isOpened():
                (status, frame) = opencv_catcher.read()
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






