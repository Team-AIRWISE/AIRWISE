import threading
from flask import Flask, render_template
from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
import sqlite3
import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize database connection
conn = sqlite3.connect("py.db")
cur = conn.cursor()

# Define Flask route
@app.route('/')
def index():
    return render_template('airwise.html', template_folder='templates')

# Define function to handle data logging
def log_data():
    while True:
        # Record data in database
        # (This part of the code is adapted from your looped() function)
        currentTime = str(datetime.datetime.now())
        temperature = bme688.readTemperature()
        humidity = bme688.readHumidity()
        co2 = bme688.readeCO2()
        aqi = bme688.getAirQualityScore()
        aqp = bme688.getAirQualityPercent()
        pressure = bme688.readPressure()

        cur.execute("INSERT INTO loggs (Time, Temperature, humidity, eco2, aqs, aqp, pressure) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (currentTime, temperature, humidity, co2, aqi, aqp, pressure))

        conn.commit()

        sleep(10)

# Start Flask app in a separate thread
def run_flask():
    app.run(debug=True, host='AIRWISE.local', port=5000)

# Start the database logging thread
def run_logging():
    log_data()

if __name__ == '__main__':
    # Create and start threads for Flask app and database logging
    flask_thread = threading.Thread(target=run_flask)
    logging_thread = threading.Thread(target=run_logging)

    flask_thread.start()
    logging_thread.start()

    # Wait for threads to finish (which they won't, so this will effectively keep the main thread alive)
    flask_thread.join()
    logging_thread.join()

    # Close database connection when finished
    conn.close()
