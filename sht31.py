import flask
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from board import I2C
from adafruit_sht31d import SHT31D

SCHEDULER = BackgroundScheduler()
APP = flask.Flask(__name__)

# Create sensor object, communicating over the board's default I2C bus
i2c = I2C()
SENSOR = SHT31D(i2c)

timestamp = None
humidity = False
temperature = False

def getReadings():
    global humidity, temperature, timestamp
    # Gather readings from the sensor.
    try:
        humidity = SENSOR.relative_humidity
        temperature = SENSOR.temperature
    # In case there's a read lag or some other read error, we'll fill it with False.
    except:
        humidity = False
        temperature = False
    timestamp = datetime.now(tz = ZoneInfo('Asia/Hong_Kong')).strftime("%Y-%m-%d %H:%M:%S")

# Schedule the first refresh in 5 seconds.
SCHEDULER.add_job(func = getReadings, trigger = "interval", seconds = 5)
SCHEDULER.start()

@APP.route('/')
def hello():
    global humidity, temperature, timestamp
    return flask.jsonify(
        timestamp = timestamp,
        temperature = temperature,
        humidity = humidity
    )

if __name__ == "__main__":
    APP.run(host = "0.0.0.0", port = '4000', debug = True)