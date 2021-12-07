export FLASK_APP=app.py
export APP_BIND="0.0.0.0"
export APP_PORT=5000

flask run --host=$APP_BIND --port=$APP_PORT