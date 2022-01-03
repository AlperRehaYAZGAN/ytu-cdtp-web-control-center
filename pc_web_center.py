#./venv/bin/python.exe

# YTU CDTP - Camera Stream Collector, Anomaly Extractor and Stream Proxy Server
# Author: Alper Reha YAZGAN
# Date: 08.12.2021

#
#   APP INTERNAL DEPENDENCIES
#
import os
import json
import time 
# dotenv
from dotenv import load_dotenv
load_dotenv( os.path.join(os.getcwd(), '.env'))

# dotenv initial values
SERVER_APP_BIND = os.getenv("SERVER_APP_BIND", "0.0.0.0")
SERVER_APP_PORT = int(os.getenv("SERVER_APP_PORT", "5000"))


#
#   Flask Web App Dependencies
#
from flask import Flask, render_template, Response
import requests
app = Flask(__name__)

#   Raspberry Pi Camera Dependencies
#
import cv2

# camera port from environment variable
CV2_STREAM_FROM_1 = os.getenv("CV2_STREAM_FROM_1","0")
# check if CV2_STREAM_FROM_1 is a valid camera port
if CV2_STREAM_FROM_1.isdigit():
    # cast to int
    CV2_STREAM_FROM_1 = int(CV2_STREAM_FROM_1)
# print CV2_STREAM_FROM_1
print("CV2_STREAM_FROM_1:", CV2_STREAM_FROM_1)
pc_stream_capture_1 = cv2.VideoCapture(CV2_STREAM_FROM_1) 
cv2.VideoWriter_fourcc('M','J','P','G')
pc_stream_capture_1.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
pc_stream_capture_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# camera port 2 from environment variable
CV2_STREAM_FROM_2 = os.getenv("CV2_STREAM_FROM_2","1")
# check if CV2_STREAM_FROM_2 is a valid camera port
if CV2_STREAM_FROM_2.isdigit():
    # cast to int
    CV2_STREAM_FROM_2 = int(CV2_STREAM_FROM_2)
# print CV2_STREAM_FROM_2
print("CV2_STREAM_FROM_2:", CV2_STREAM_FROM_2)
pc_stream_capture_2 = cv2.VideoCapture(CV2_STREAM_FROM_2) 
pc_stream_capture_2.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
pc_stream_capture_2.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)


#
#   Socket Implementation
#
from flask_socketio import SocketIO
sio = SocketIO(app)

# @sio.on('connect')
def on_connect():
    print("Client connected")
sio.on('connect', on_connect)


# disconnect
# @sio.on('disconnect')
def on_disconnect():
    print("Client disconnected")
sio.on('disconnect', on_disconnect)


# on error
@sio.on_error()
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))


# on anomaly-button-1-clicked
@sio.on('anomaly-button-1-clicked')
def anomaly_button_1_clicked(data):
    sio.emit('anomaly-button-1-clicked', data)
    print("Anomaly Button 1 Clicked")
    pass

# on anomaly-button-2-clicked
@sio.on('anomaly-button-2-clicked')
def anomaly_button_2_clicked(data):
    sio.emit('anomaly-button-2-clicked', data)
    print("Anomaly Button 2 Clicked")
    pass

# start time
start_time = time.time()


# GET / - return running app info
@app.route('/')
def system_status():
    # Status of system as json { "system" : "up", "status" : "ok", "startTime" : "2020-12-08T12:00:00", uptime : "68sec" }
    uptime = time.time() - start_time
    uptime = str(round(uptime,2)) + "sec"
    # return info as json
    return json.dumps({
        "service" : "server-anomaly-stream-proxy", 
        "system" : "up",
        "status" : True, 
        "startTime" : time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(start_time)), 
        "uptime" : uptime,
        "monitorUrl": "/monitor"
    })



"""Web UI for displaying camera streams.""" 
# GET /monitor - return monitor page to display camera
@app.route('/monitor') 
def index(): 
   return render_template('index-url.html', stream_url_1 = "/anomaly_stream_1", stream_url_2 = "/anomaly_stream_2")


"""Catch CV2_STREAM_FROM_1, find anomaly on image then return as jpeg image for displaying.""" 
# stream_camera_frame - Streams the camera video feed as a jpeg image
def proxy_frame_1(): 
    while True: 
        success, frame = pc_stream_capture_1.read() 
        try:
            ret, buffer = cv2.imencode('.jpg', frame) #, cv2.flip(frame,1))
            frame = buffer.tobytes()
            # frame uzerinde sekiller falan ekle
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Break-1:",e)
            break
        pass
    pass

# GET /anomaly_stream_1 - catch stream from camera 1 then return as jpeg image
@app.route('/anomaly_stream_1') 
def video_stream_1(): 
   return Response(proxy_frame_1(), mimetype='multipart/x-mixed-replace; boundary=frame') 


"""Catch CV2_STREAM_FROM_2, find anomaly on image then return as jpeg image for displaying.""" 
def proxy_frame_2(): 
    while True: 
        success, frame = pc_stream_capture_2.read() 
        try:
            ret, buffer = cv2.imencode('.jpg', frame) #, cv2.flip(frame,1))
            frame = buffer.tobytes()
            # frame uzerinde sekiller falan ekle
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Break-2:",e)
            break
        pass
    pass

# GET /anomaly_stream_2 - catch stream from camera 2 then return as jpeg image for displaying.
@app.route('/anomaly_stream_2') 
def video_stream_2(): 
   return Response(proxy_frame_2(), mimetype='multipart/x-mixed-replace; boundary=frame') 


# flask main function
if __name__ == '__main__':
    print("PC Server initializing...")
    # run from dotenv
    app.run(app,host=SERVER_APP_BIND,port=SERVER_APP_PORT)
    print("PC Server Port: ", SERVER_APP_PORT)
    # run socket
    sio.run(app)
    print("PC Server Initialization Finished")
    pass