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
# camera port 2 from environment variable
CV2_STREAM_FROM_2 = os.getenv("CV2_STREAM_FROM_2","1")

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
        "service" : "stream-proxy-server", 
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
   return render_template('index-url.html', stream_url_1 = "/proxy_stream_1", stream_url_2 = "/proxy_stream_2")



@app.route("/proxy_stream_1")
def streamed_proxy():
    r = requests.get(CV2_STREAM_FROM_1, stream=True)
    return Response(r.iter_content(chunk_size=10*1024),
                    content_type=r.headers['Content-Type']
    )

@app.route("/proxy_stream_2")
def streamed_proxy():
    r = requests.get(CV2_STREAM_FROM_2, stream=True)
    return Response(r.iter_content(chunk_size=10*1024),
                    content_type=r.headers['Content-Type']
    )


def main():
    print("Starting main...")

# flask main function
if __name__ == '__main__':
    print("PC Server initializing...")
    # run from dotenv
    app.run(app,host=SERVER_APP_BIND,port=SERVER_APP_PORT)
    print("PC Server Port: ", SERVER_APP_PORT)
    print("PC Server Initialization Finished")
    pass