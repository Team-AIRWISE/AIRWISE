from time import sleep
from KitronikAirQualityControlHAT import *
bme688 = KitronikBME688()
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)


oled.image = Image.open("kitronik-logo.jpg")
oled.show()
sleep(5)
oled.clear()

bme688.measureData()
humidity=bme688.readHumidity()
c02=bme688.readeCO2()
bme688.getAirQualityPercent()

if humdity<43:
  hpo1.turnOn()
elif humidity>47:
  hpo2.turnOn()
else:
  KitronikHighPowerOut(1)
  hpo1.turnOff()
  hpo2.turnOff()

if c02>800:
  
