from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
'''import sqlite3
from sqlite3 import Error'''
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
#Read Air quality levels

bme688.measureData()
bme688.calcBaselines(oled)
humidity=bme688.readHumidity()
#c02=bme688.readeCO2()
aqp=bme688.getAirQualityPercent()
temperature=bme688.readTemperature()
aqi=bme688.getAirQualityScore()
Pressure=bme688.readPressure()
'''
#Water level check TBF

#Humidity correction

if humidity<43:
  hpo1.turnOn()
elif humidity>47:
  hpo2.turnOn()
else:
  KitronikHighPowerOut(1)
  hpo1.turnOff()
  hpo2.turnOff()

#C02 level Warning
if c02>800 and c02<1000:
  oled.displayText("C02 levels are high", 1)
  oled.displayText("Caution!", 2)
  buzzer.start()
  for i in range(4):
    buzzer.changeTone(440)
    sleep(1)
    buzzer.changeTone(220)
    sleep(1)
  buzzer.stop()
  c02High=True
elif c02>1000:
  oled.displayText("C02 levels are EXTREMELY HIGH", 1)
  oled.displayText("EVACUATE AREA IMMEDIATELY", 2)
  buzzer.start()
  while c02>1000:
    buzzer.changeTone(440)
    sleep(1)
    buzzer.changeTone(220)
    sleep(1)

#AQI level Warning

if aqi>150 and aqi<200:
  oled.displayText("Air Quality levels are unhealthy", 1)
  oled.displayText("Caution!", 2)
  buzzer.start()
  for i in range(4):
    buzzer.changeTone(440)
    sleep(1)
    buzzer.changeTone(220)
    sleep(1)
  buzzer.stop()
  c02High=True
elif aqi>200:
  oled.displayText("Air Quality levels are EXTREMELY unhealthy", 1)
  oled.displayText("EVACUATE AREA IMMEDIATELY", 2)
  buzzer.start()
  while aqi>200:
    buzzer.changeTone(440)
    sleep(1)
    buzzer.changeTone(220)
    sleep(1)
'''
#Record data in spreadsheet
'''    def create_connection(path):
    connection = None
    try:
        connection = database.sqlite
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
'''

#upload info to HTML website