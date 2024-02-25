from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
import sqlite3
import datetime
humidOn=False
#connect to database

conn = sqlite3.connect("py.db")
cur = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
loggs(Time TEXT PRIMARY KEY, Temperature REAL, humidity REAL, eco2 REAL, aqs REAL, aqp REAL, pressure REAL)"""
cur.execute(command1)

#define modules

bme688 = KitronikBME688()
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)
buzzer = KitronikBuzzer()

#Display AIRWISE logo

oled.image = Image.open("AIRWISE_logo.jpg")
oled.image = oled.image.convert('1')
oled.show()
sleep(5)
oled.clear()
oled.show()

#Calibrate sensor

bme688.calcBaselines(oled)

#Looped code

def looped(humidOn):
    
  #Read Air quality levels

  bme688.measureData()
  bme688.readHumidity()
  bme688.readeCO2()
  bme688.getAirQualityPercent()
  bme688.readTemperature()
  bme688.getAirQualityScore()
  bme688.readPressure()

  #Display air quality levels

  oled.clear()
  oled.displayText("Temperature:" + str(bme688.readTemperature()), 1)
  oled.displayText("Pressure:" + str(bme688.readPressure()), 2)
  oled.displayText("Humidity:"+  str(bme688.readHumidity()), 3)
  oled.displayText("eCO2:" + str(bme688.readeCO2()), 4)
  oled.displayText("Air Quality %:" + str(bme688.getAirQualityPercent()), 5)
  oled.displayText("Air Quality Score:" + str(bme688.getAirQualityScore()), 6)
  oled.show()

  #Water level check TBF

  #Humidity correction

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
    hpo1.turnOn()

  elif bme688.readHumidity()<43:
    if humidOn==False:
      hpo2.turnOn()
      sleep(0.2)
      hpo2.turnOff()
      humidOn=True
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

  #C02 level Warning
      
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

  cur.execute("INSERT INTO loggs (Time, Temperature, humidity, eco2, aqs, aqp, pressure) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (currentTime, temperature, humidity, co2, aqi, aqp, pressure))

  conn.commit()


#upload info to HTML website

while 1==1:
  looped(humidOn)
  sleep(10)

conn.close()