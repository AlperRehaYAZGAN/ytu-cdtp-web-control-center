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
# dotenv
from dotenv import load_dotenv
load_dotenv(dotenv_path= getcwd() + '/' + '.env')

# dotenv initial values
PC_APP_BIND = getenv("PC_APP_BIND","0.0.0.0")
PC_APP_PORT = int(getenv("PC_APP_PORT","5000"))

PI_STREAM_HOST = getenv("PI_STREAM_HOST", "localhost")
PI_STREAM_PORT = int(getenv("PI_STREAM_PORT", "5000"))
PI_STREAM_URL = getenv("PI_STREAM_URL","/video_feed")

# print env vars
print("PC_APP_BIND:", PC_APP_BIND)
print("PC_APP_PORT:", PC_APP_PORT)
print("PI_STREAM_HOST:", PI_STREAM_HOST)
print("PI_STREAM_PORT:", PI_STREAM_PORT)
print("PI_STREAM_URL:", PI_STREAM_URL)




#
#   Flask Web App Dependencies
#
from flask import Flask, render_template, Response , stream_with_context
import requests
app = Flask(__name__)

# start time
start_time = time.time()

# flask main function
if __name__ == '__main__':
    print("PC Server initializing...")
    # run from dotenv
    app.run(app,host=PC_APP_BIND,port=PC_APP_PORT)
    print("PC Server Port: ", PC_APP_PORT)
    print("PC Server Initialization Finished")
    pass

def on_anomalia(data):
    # decode incoming data ({"status" : "ANOMALY_CAR_EXPLOIDATION", "time" : "2020-12-08T12:00:00.000Z"})
    data_anomaly = json.loads(data)
    # get status if exist
    if "status" in data_anomaly:
        # get status
        anomaly_status = data_anomaly["status"]
        # get time
        issued_at = data_anomaly["time"]
        # print anomaly
        print("Anomaly:", anomaly_status, "at", issued_at)
        # handle anomaly
        # handle(anomaly_status, issued_at)
        pass
    else:
        print("No anomaly data found")
        pass
    pass


# GET / - return running app info
@app.route('/')
def system_status():
    # Status of system as json { "system" : "up", "status" : "ok", "startTime" : "2020-12-08T12:00:00", uptime : "68sec" }
    uptime = time.time() - start_time
    uptime = str(round(uptime,2)) + "sec"
    # return info as json
    return json.dumps({
        "service" : "pc-camera-proxy-service", 
        "system" : "up",
        "status" : True, 
        "startTime" : time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(start_time)), 
        "uptime" : uptime,
        "monitorUrl": "/monitor"
    })



"""Video streaming .""" 
# GET /monitor - return monitor page to display camera
@app.route('/monitor') 
def index(): 
   return render_template('index.html')



CAMERA_STREAM_URL = "http://" + PI_STREAM_HOST + ":" + str(PI_STREAM_PORT) + PI_STREAM_URL
@app.route("/proxy_stream")
def streamed_proxy():
    r = requests.get(CAMERA_STREAM_URL, stream=True)
    return Response(r.iter_content(chunk_size=10*1024),
                    content_type=r.headers['Content-Type'])




def main():
    print("Starting main...")

# flask main function
if __name__ == '__main__':
    print("App initializing...")
    main()
    pass