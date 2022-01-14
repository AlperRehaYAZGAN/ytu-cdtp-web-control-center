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
app = Flask(__name__)

#   Raspberry Pi Camera Dependencies
#
import cv2
# print opencv version
print("OpenCV version: {}".format(cv2.__version__))

# path to video and cascade model
car_cascade_src = os.path.join(os.getcwd(), 'haarcascades','cars.xml')
fire_cascade_src = os.path.join(os.getcwd(), 'haarcascades','fire.xml')
human_frontface_src = os.path.join(os.getcwd(), 'haarcascades','human_frontface.xml')
fullbody_src = os.path.join(os.getcwd(), 'haarcascades','fullbody.xml')
# print paths
print("Cascade path: {}".format(car_cascade_src))
print("Cascade path: {}".format(fire_cascade_src))
print("Cascade path: {}".format(human_frontface_src))
print("Cascade path: {}".format(fullbody_src))
# CASCADE CLASSIFIER
car_cascade = cv2.CascadeClassifier(car_cascade_src)
fire_cascade = cv2.CascadeClassifier(fire_cascade_src)
frontface_cascade = cv2.CascadeClassifier(human_frontface_src)
fullbody_cascade = cv2.CascadeClassifier(fullbody_src)

# camera port from environment variable
CV2_STREAM_FROM_1 = int(os.getenv("CV2_STREAM_FROM_1",0))
"""
# check if CV2_STREAM_FROM_1 is a valid camera port
if CV2_STREAM_FROM_1.isdigit():
    # cast to int
    CV2_STREAM_FROM_1 = int(CV2_STREAM_FROM_1)
"""
# print CV2_STREAM_FROM_1
print("CV2_STREAM_FROM_1:", CV2_STREAM_FROM_1)
pc_stream_capture_1 = cv2.VideoCapture(CV2_STREAM_FROM_1,cv2.CAP_DSHOW) 
pc_stream_capture_1.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
pc_stream_capture_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# camera port 2 from environment variable
CV2_STREAM_FROM_2 = int(os.getenv("CV2_STREAM_FROM_2",0))
"""
# check if CV2_STREAM_FROM_2 is a valid camera port
if CV2_STREAM_FROM_2.isdigit():
    # cast to int
    CV2_STREAM_FROM_2 = int(CV2_STREAM_FROM_2)
"""
# print CV2_STREAM_FROM_2
print("CV2_STREAM_FROM_2:", CV2_STREAM_FROM_2)
pc_stream_capture_2 = cv2.VideoCapture(CV2_STREAM_FROM_2,cv2.CAP_DSHOW) 
pc_stream_capture_2.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
pc_stream_capture_2.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
if not pc_stream_capture_1.isOpened():
    print("Unable to open camera stream 1")
    exit()
if not pc_stream_capture_2.isOpened():
    print("Unable to open camera stream 2")
    exit()

import time
import serial
from crccheck.crc import Crc32Mpeg2
from multiprocessing import Queue

import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print ("port: ",p)

class SerialCom:
    def __init__(self, port="COM3", baud=9600, msgsize=7,):
        while True:
            try:
                self.s = serial.Serial(port, baud)
                break
            except Exception as e:
                print("port yok!", e)

        self.msgsize = msgsize
        self.q = Queue(10)
        self.sendmsg = []

        self.header1 = 0b0100
        self.header2 = 0b0101

    def writeSerialPort(self, q):
        try:
            self.sendmsg = q.get(timeout=0.001)
        except:
            pass

        if len(self.sendmsg) > 0:
            self.sendmsg.insert(0, self.header1)
            self.sendmsg.insert(1, self.header2)

            calcCrc = Crc32Mpeg2.calc(self.sendmsg)

            first = (calcCrc >> 24) & 0xFF
            second = (calcCrc >> 16) & 0xFF
            third = (calcCrc >> 8) & 0xFF
            fourth = (calcCrc & 0xFF)

            self.sendmsg.append(first)
            self.sendmsg.append(second)
            self.sendmsg.append(third)
            self.sendmsg.append(fourth)

            self.s.write(self.sendmsg)
            s = list(self.sendmsg)
            print(s)
            self.sendmsg = []

port = SerialCom()
msgQueue = Queue(10)

from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)
cache.init_app(app)

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
    # log anomaly-button-1-clicked
    print("Area-1 Anomaly Order:", data)
    # button clicked
    if( data["type"] == "REFRESH" ):
        sio.emit('anomaly-button-1-clicked', {"type": "REFRESH"})
        msgQueue.put([4])
        port.writeSerialPort(msgQueue)
    elif( data["type"] != "TEST" ):
        msgQueue.put([1])
        port.writeSerialPort(msgQueue)

    sio.emit('anomaly-button-1-clicked', data)
    pass

# on anomaly-btn-1-test-clicked
@sio.on('anomaly-btn-1-test-clicked')
def anomaly_button_1_clicked(data):
    # log anomaly-button-1-clicked
    print("Anomaly-button-1-test-clicked:", data)
    sio.emit('anomaly-button-1-clicked', {'type': 'TEST'})
    pass

# on anomaly-button-2-clicked
@sio.on('anomaly-button-2-clicked')
def anomaly_button_2_clicked(data):
    # log anomaly-button-2-clicked
    print("Area-2 Anomaly Order:", data)
    # button clicked
    if( data["type"] == "REFRESH" ):
        sio.emit('anomaly-button-1-clicked', {"type": "REFRESH"})
        msgQueue.put([4])
        port.writeSerialPort(msgQueue)
    elif( data["type"] != "TEST" ):
        msgQueue.put([3])
        port.writeSerialPort(msgQueue)
    sio.emit('anomaly-button-2-clicked', data)
    pass

# on anomaly-btn-2-test-clicked
@sio.on('anomaly-btn-2-test-clicked')
def anomaly_button_1_clicked(data):
    # log anomaly-button-2-test-clicked
    print("Anomaly-button-2-test-clicked:", data)
    sio.emit('anomaly-button-2-clicked', { 'type': 'TEST' })
    pass

# on camera-1-request
@sio.on('camera-1-request')
def camera_1_change_cascade(data):
    # log data
    print("camera-1-request:", data)
    changeTo = int(data["to"])
    if(changeTo != 0 and changeTo > 0 and changeTo < 5):
        cache.set("req_camera_1", changeTo)
        sio.emit('camera-1-changed', {"to": int(cache.get("req_camera_1"))})
        pass
    pass

# on camera-2-request
@sio.on('camera-2-request')
def camera_2_change_cascade(data):
    # log data
    print("camera-2-request:", data)
    changeTo = int(data["to"])
    if(changeTo != 0 and changeTo > 0 and changeTo < 5):
        cache.set("req_camera_2", changeTo)
        sio.emit('camera-2-changed', {"to": int(cache.get("req_camera_2"))})
        pass
    pass

# on show-display
@sio.on('show-display')
def show_display_text(data):
    displayText = str(data["text"])
    sio.emit('show-lcd-display', {"text": displayText})
    pass

# start time
start_time = time.time()
# checkpoints for anomaly detection

cache.set('req_camera_1',1)
cache.set('req_camera_2',1)
cp_exit_road_1 = time.time()
cp_exit_road_2 = time.time()
cp_fire_1 = time.time()
cp_fire_2 = time.time()
cp_human_on_road_1 = time.time()
cp_human_on_road_2 = time.time()


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
   return render_template('monitor.html', stream_url_1 = "/anomaly_stream_1", stream_url_2 = "/anomaly_stream_2")



def proxy_frame_normal_1(): 
    while True: 
        try:
            global cp_fire_1, cp_exit_road_1, cp_human_on_road_1,pc_stream_capture_1,req_camera_1
            success, frame = pc_stream_capture_1.read() 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            req_camera_1 = int(cache.get("req_camera_1"))

            if (req_camera_1 == 2):
                # 2 is fire anomaly
                fires = fire_cascade.detectMultiScale(gray,1.1,1)
                # fire finder
                for (x,y,w,h) in fires:
                    cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
                    if (time.time() - cp_fire_1) > 3:
                        sio.emit("anomaly-detected-1", {"type": "ANOMALY_FIRE_EXIST"})
                        cp_fire_1 = time.time()
                        pass
                    pass
                pass
            elif (req_camera_1 == 3):
                # 3 is car exit road anomaly
                cars = car_cascade.detectMultiScale(gray,1.1,1)

                # highway line borders
                # left border is 1/4 of the screen width, right border is 3/4 of the screen width. 
                # Notify with blue line
                cv2.line(frame, (int(frame.shape[1]/7), 0), (int(frame.shape[1]/7), frame.shape[0]), (255, 0, 0), 2)
                cv2.line(frame, (int(frame.shape[1]*6/7), 0), (int(frame.shape[1]*6/7), frame.shape[0]), (255, 0, 0), 2)
                # car finder
                for (x,y,w,h) in cars:
                    # check if vehicle exit from highway line (left border or right border)
                    # if attached to left border, vehicle is leaving from highway red box
                    # if attached to right border, vehicle is leaving from highway red box
                    # otherwise, vehicle is staying on highway green box
                    if (x < int(frame.shape[1]/7)):
                        # anomaly var
                        if (w > 50 and h > 50):
                            if (time.time() - cp_exit_road_1) > 3:
                                sio.emit("anomaly-detected-1", {"type": "ANOMALY_CAR_EXIT_ROAD"})
                                cp_exit_road_1 = time.time()
                            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        # opencv color rgb is BGR
                        pass
                    elif (x > int(frame.shape[1]*6/7)):
                        # anomaly var
                        if (time.time() - cp_exit_road_1) > 3:
                            sio.emit("anomaly-detected-1", {"type": "ANOMALY_CAR_EXIT_ROAD"})
                            cp_exit_road_1 = time.time()
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        pass
                    else:
                        # rectangle color is green
                        # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        pass
                    pass
                pass
            elif (req_camera_1 == 4):
                # 4 is human on road anomaly
                fullbodies = fullbody_cascade.detectMultiScale(gray,1.1,1)
                # fullbody finder
                for (x,y,w,h) in fullbodies:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    if (time.time() - cp_human_on_road_1) > 3:
                        sio.emit('anomaly-detected-1', {'type': 'ANOMALY_HUMAN_ON_ROAD'})
                        cp_human_on_road_1 = time.time()
                        pass
                    pass
                pass
            else:
                # 1 is normal
                pass
                    

            ret, buffer = cv2.imencode('.jpg', frame) #, cv2.flip(frame,1))
            frame = buffer.tobytes()
            # frame uzerinde sekiller falan ekle
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Break-normal-1:",e)
            break
        pass
    pass

# GET /anomaly_stream_1 - catch stream from camera 1 then return as jpeg image
@app.route('/anomaly_stream_1') 
def video_stream_1(): 
   return Response(proxy_frame_normal_1(), mimetype='multipart/x-mixed-replace; boundary=frame') 

def proxy_frame_normal_2(): 
    while True: 
        try:
            global cp_fire_2, cp_exit_road_2, cp_human_on_road_2,pc_stream_capture_2
            req_camera_2 = int(cache.get("req_camera_2"))
            success, frame = pc_stream_capture_2.read() 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if (req_camera_2 == 2):
                # 2 is fire anomaly
                fires = fire_cascade.detectMultiScale(frame,1.1,1)
                # fire finder
                for (x,y,w,h) in fires:
                    cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
                    if (time.time() - cp_fire_2) > 3:
                        sio.emit("anomaly-detected-2", {"type": "ANOMALY_FIRE_EXIST"})
                        cp_fire_2 = time.time()
                        pass
                    pass
                pass
            elif (req_camera_2 == 3):
                # 3 is car exit road anomaly
                cars = car_cascade.detectMultiScale(gray,1.1,1)

                # highway line borders
                # left border is 1/4 of the screen width, right border is 3/4 of the screen width. 
                # Notify with blue line
                cv2.line(frame, (int(frame.shape[1]/7), 0), (int(frame.shape[1]/7), frame.shape[0]), (255, 0, 0), 2)
                cv2.line(frame, (int(frame.shape[1]*6/7), 0), (int(frame.shape[1]*6/7), frame.shape[0]), (255, 0, 0), 2)
                # car finder
                for (x,y,w,h) in cars:
                    # check if vehicle exit from highway line (left border or right border)
                    # if attached to left border, vehicle is leaving from highway red box
                    # if attached to right border, vehicle is leaving from highway red box
                    # otherwise, vehicle is staying on highway green box
                    if (x < int(frame.shape[1]/5) or x > int(frame.shape[1]*6/7)):
                        # anomaly var
                        # if found anomly size is bigger than 25 px
                        if (w > 50 and h > 50):
                            if (time.time() - cp_exit_road_2) > 3:
                                sio.emit("anomaly-detected-2", {"type": "ANOMALY_CAR_EXIT_ROAD"})
                                cp_exit_road_2 = time.time()
                            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        pass
                    else:
                        # rectangle color is green
                        # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        pass
                    pass
                pass
            elif (req_camera_2 == 4):
                # 4 is human on road anomaly
                fullbodies = fullbody_cascade.detectMultiScale(gray,1.1,1)
                # fullbody finder
                for (x,y,w,h) in fullbodies:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    if (time.time() - cp_human_on_road_2) > 3:
                        sio.emit('anomaly-detected-2', {'type': 'ANOMALY_HUMAN_ON_ROAD'})
                        cp_human_on_road_2 = time.time()
                        pass
                    pass
                pass
            else:
                # 1 is normal
                pass
                    

            ret, buffer = cv2.imencode('.jpg', frame) #, cv2.flip(frame,1))
            frame = buffer.tobytes()
            # frame uzerinde sekiller falan ekle
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Break-normal-2:",e)
            break
        pass
    pass

# GET /anomaly_stream_2 - catch stream from camera 2 then return as jpeg image for displaying.
@app.route('/anomaly_stream_2') 
def video_stream_2(): 
   return Response(proxy_frame_normal_2(), mimetype='multipart/x-mixed-replace; boundary=frame') 


# flask main function
if __name__ == '__main__':
    try:
        print("PC Server initializing...")
        # run from dotenv
        app.run(app,host=SERVER_APP_BIND,port=SERVER_APP_PORT)
        print("PC Server Port: ", SERVER_APP_PORT)
        # run socket
        sio.run(app)
        print("PC Server Initialization Finished")
    except Exception as e:
        print("PC Server Initialization Failed: ", e)
        pass
    pass