#import libraries
from flask import Flask, render_template
from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
import sqlite3
import datetime
from threading import Thread
humidOn = False

# Define modules
bme688 = KitronikBME688()
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)
buzzer = KitronikBuzzer()

# Calibrate sensor
bme688.calcBaselines(oled)
bme688.measureData()

# Host website
app = Flask(__name__)

@app.route('/')
def index():
  bme688.measureData()
  return render_template('airwise.html', template_folder='templates', humidity=bme688.readHumidity(), co2=bme688.readeCO2(), temperature=bme688.readTemperature(), aqp=bme688.getAirQualityPercent(), pressure=bme688.readPressure())

#loop with calibration check

def run_loop():
  print("debug")
  calibration = 0
  global humidOn
  while True:
    bme688.measureData()
    bme688.readHumidity()
    bme688.readeCO2()
    bme688.getAirQualityPercent()
    bme688.readTemperature()
    bme688.getAirQualityScore()
    bme688.readPressure()
    
    calibration=calibration+1
    if calibration>1000:
      print("debug")
      humidOn = looped(humidOn)

#process to be looped

def looped(humidOn):
    
  # Connect to database
  conn = sqlite3.connect("py.db")
  cur = conn.cursor()
  command1 = """CREATE TABLE IF NOT EXISTS
  loggs(Time TEXT PRIMARY KEY, Temperature REAL, humidity REAL, eco2 REAL, aqs REAL, aqp REAL, pressure REAL)"""
  cur.execute(command1)

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
  oled.displayText("Humidity:" + str(bme688.readHumidity()), 2)
  oled.displayText("eCO2:" + str(bme688.readeCO2()), 3)
  oled.displayText("Air Quality %:" + str(bme688.getAirQualityPercent()), 4)
  oled.displayText("AQI:" + str(bme688.getAirQualityScore()), 5)
  oled.show()

  # Water level check TBF

  # Humidity correction
  if bme688.readHumidity()>47:
    if humidOn==True:
      hpo2.turnOn()
      sleep(0.2)
      hpo2.turnOff()
      sleep(1)
      hpo2.turnOn()
      sleep(0.2)
      hpo2.turnOff()
      humidOn=False
      print("humidifier off")
    hpo1.turnOn()

  elif bme688.readHumidity()<43:
    if humidOn==False:
      hpo2.turnOn()
      sleep(0.2)
      hpo2.turnOff()
      humidOn=True
      print("humidifier on")
    hpo1.turnOff()

  else:
    hpo1.turnOff()
    if humidOn==True:
      hpo2.turnOn()
      sleep(0.2)
      hpo2.turnOff()
      sleep(1)
      hpo2.turnOn()
      sleep(0.2)
      hpo2.turnOff()
      humidOn=False
      print("humidifier off")

  #co2 level warning
      
  if bme688.readeCO2()>800 and bme688.readeCO2()<1000:
    oled.clear()
    oled.displayText("C02 levels are high", 1)
    oled.displayText("Caution!", 2)
    oled.show()
    buzzer.start()
    for i in range(4):
      buzzer.changeTone(440)
      sleep(1)
      buzzer.changeTone(220)
      sleep(1)
    buzzer.stop()
    c02High=True

  elif bme688.readeCO2()>1000:
    print(bme688.readeCO2())
    oled.clear()
    oled.displayText("C02 levels are EXTREMELY HIGH", 1)
    oled.displayText("EVACUATE AREA IMMEDIATELY", 2)
    oled.show()
    buzzer.start()
    while bme688.readeCO2()>1000:
      buzzer.changeTone(440)
      sleep(1)
      buzzer.changeTone(220)
      sleep(1)

  #AQI level Warning

  if bme688.getAirQualityScore()>150 and bme688.getAirQualityScore()<200:
    oled.clear()
    oled.displayText("Air Quality levels are unhealthy", 1)
    oled.displayText("Caution!", 2)
    oled.show()
    buzzer.start()
    for i in range(4):
      buzzer.changeTone(440)
      sleep(1)
      buzzer.changeTone(220)
      sleep(1)
    buzzer.stop()
    c02High=True
  elif bme688.getAirQualityScore()>200:
    oled.clear()
    oled.displayText("Air Quality levels are EXTREMELY unhealthy", 1)
    oled.displayText("EVACUATE AREA IMMEDIATELY", 2)
    oled.show()
    buzzer.start()
    while bme688.getAirQualityScore()>200:
      buzzer.changeTone(440)
      sleep(1)
      buzzer.changeTone(220)
      sleep(1)

  #Record data in database
      
  currentTime = str(datetime.datetime.now())
  temperature = bme688.readTemperature()
  humidity = bme688.readHumidity()
  co2 = bme688.readeCO2()
  aqi = bme688.getAirQualityScore()
  aqp = bme688.getAirQualityPercent()
  pressure = bme688.readPressure()

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

#run website and sensor values in seperate threads(processes)

if __name__ == '__main__':
    print("debug1")
    thread = Thread(target=run_loop)
    print("debug2")
    thread.start()
    print("debug3")
    app.run(host='AIRWISE.local', port=5000)

conn.close()
