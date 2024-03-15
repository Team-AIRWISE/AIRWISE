from flask import Flask, render_template
from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
import sqlite3
import datetime
from threading import Thread

humidOn = False
calibration = 0

# Define modules
bme688 = KitronikBME688()
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)
buzzer = KitronikBuzzer()

# Connect to database
conn = sqlite3.connect("py.db")
cur = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
loggs(Time TEXT PRIMARY KEY, Temperature REAL, humidity REAL, eco2 REAL, aqs REAL, aqp REAL, pressure REAL)"""
cur.execute(command1)

# Calibrate sensor
bme688.calcBaselines(oled)
bme688.measureData()
bme688.readHumidity()
bme688.readeCO2()
bme688.getAirQualityPercent()
bme688.readTemperature()
bme688.getAirQualityScore()
bme688.readPressure()

# Host website
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('airwise.html', template_folder='templates')

def run_loop():
    global humidOn
    while True:
        if 1 == 1:
            print("debug")
            humidOn = looped(humidOn)
        sleep(10)

def looped(humidOn):
    # Read Air quality levels
    bme688.measureData()
    bme688.readHumidity()
    bme688.readeCO2()
    bme688.getAirQualityPercent()
    bme688.readTemperature()
    bme688.getAirQualityScore()
    bme688.readPressure()

    # Display air quality levels
    oled.clear()
    oled.displayText("Temperature:" + str(bme688.readTemperature()), 1)
    oled.displayText("Pressure:" + str(bme688.readPressure()), 2)
    oled.displayText("Humidity:" + str(bme688.readHumidity()), 3)
    oled.displayText("eCO2:" + str(bme688.readeCO2()), 4)
    oled.displayText("Air Quality %:" + str(bme688.getAirQualityPercent()), 5)
    oled.displayText("Air Quality Score:" + str(bme688.getAirQualityScore()), 6)
    oled.show()

    # Water level check TBF

    # Humidity correction
    # Your humidity correction logic goes here

    # Record data in database
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

    return humidOn

if __name__ == '__main__':
    thread = Thread(target=run_loop)
    thread.start()
    app.run(debug=True, host='AIRWISE.local', port=5000)

conn.close()
