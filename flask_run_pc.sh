export PC_APP_BIND="0.0.0.0"
export PC_APP_PORT=5000
export PI_STREAM_HOST="localhost"
export PI_STREAM_PORT=5001
export PI_STREAM_URL="video_feed"

export FLASK_APP=pc_stream_proxy.py
flask run --host=$PC_APP_BIND --port=$PC_APP_PORT