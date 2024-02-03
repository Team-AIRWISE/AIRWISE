from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
import pymysql
bme688 = KitronikBME688()
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)
buzzer = KitronikBuzzer()

#Display AIRWISE logo

oled.image = Image.open("kitronik-logo.jpg")
oled.show()
sleep(5)
oled.clear()

#Read Air quality levels

bme688.measureData()
humidity=bme688.readHumidity()
c02=bme688.readeCO2()
bme688.getAirQualityPercent()

#Water level check TBF

#Humidity correction

if humdity<43:
  hpo1.turnOn()
elif humidity>47:
  hpo2.turnOn()
else:
  KitronikHighPowerOut(1)
  hpo1.turnOff()
  hpo2.turnOff()

#C02 level Warning
if c02>800 AND c02<1000:
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
  buzzer.start()
  while 1==1:
    buzzer.changeTone(440)
    sleep(1)
    buzzer.changeTone(220)
    sleep(1)


#Record data in spreadsheet
    

#upload info to HTML website