# YTU CDTP Web Control Server
# Author: Alper Reha YAZGAN
# Date: 08.12.2021

#
#   APP INTERNAL DEPENDENCIES
#
import time 
import os
import json
# dotenv
from dotenv import load_dotenv
load_dotenv()

# dotenv initial values
APP_PORT = int(os.getenv("APP_PORT", "5001"))
APP_BIND = os.getenv("APP_BIND", "0.0.0.0")
CAMERA_STREAM_URLS = os.getenv("RASP_CAMERA_URLS", "http://127.0.0.1:5000/stream").split(",")

#
#   FLASK APP IMLEMENTATION
#
from flask import Flask,request,render_template
app = Flask(__name__)

#
#   SOCKET IO IMPLEMENTATION
#
from flask_socketio import SocketIO,send,emit
socketio = SocketIO(app)


# start time
start_time = time.time()


# flask main function
if __name__ == '__main__':
    print("App initiliazing...")
    # run from dotenv
    app.run(app,host=APP_BIND,port=APP_PORT)
    print("App Server Port: " + APP_PORT)
    socketio.run(app)
    print("Socket Server Port: " + APP_PORT)
    print("App Initialization Finished")
    pass


#
#   FLASK APP ROUTES
#

# GET / - return running app info
@app.route('/')
def system_status():
    # Status of system as json { "system" : "up", "status" : "ok", "startTime" : "2020-12-08T12:00:00", uptime : "68sec" }
    uptime = time.time() - start_time
    uptime = str(round(uptime,2)) + "sec"
    # return info as json
    return json.dumps({
        "service" : "monitor-service",
        "system" : "up", 
        "status" : True, 
        "startTime" : time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(start_time)), 
        "uptime" : uptime
    })


# GET /monitor - return monitor page
@app.route('/monitor')
def monitor_page():
    return render_template("monitor.html", streams = CAMERA_STREAM_URLS)
