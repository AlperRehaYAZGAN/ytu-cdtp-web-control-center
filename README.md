# YTU CDTP Web Control Center  

This project aiming to create a web ui and web backend for collect camera streams from raspberry pi or other sources then convert as opencv jpeg image. After convertion of stream, detect anomaly of picture and show it in the Web UI. If anomaly occurs, emit ANOMALY_DETECTED events to notify sub systems.  

This project uses venv for manage python virtual environment so follow this guideline.  

# 1-Install venv and Create venv
- https://docs.python.org/3/library/venv.html  
- pip install virtualenv
- python -m venv venv
- (Windows) .\venv\Scripts\activate
- (Linux) source ./venv/bin/activate
- You are ready to go!!!

# 2-Usage
- Go to project directory via activated venv cli
- `pip install -r requirements.txt`
- `cp .env-example > .env` (fill custom env if required)
- Windows `set FLASK_APP=pc_web_center.py` - Linux `export FLASK_APP=pc_web_center.py`
- run `python -m flask run`

# 3-Env  
Default Env  

````
SERVER_APP_BIND="0.0.0.0"
SERVER_APP_PORT="5000"
CV2_STREAM_FROM_1="http://localhost:5001/video_feed_1" -> enter raspberry pi stream url or local digit camera port
CV2_STREAM_FROM_2="http://localhost:5001/video_feed_2" -> enter raspberry pi stream url or local digit camera port
```  

# 4-URLs
GET / - Server Status  
GET /monitor - Monitor Highway Interface  
GET /anomaly_stream_1 - Stream of first camera
GET /anomaly_stream_2 - Stream of second camera



![monitor-webpage-sample](./utils/monitor-html-sample.jpg)

