from time import sleep
from KitronikAirQualityControlHAT import *
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)


oled.image = Image.open("kitronik-logo.jpg")
oled.show()
sleep(5)
oled.clear()

bme688 = KitronikBME688()
humidity=bme688.readHumidity()
if humdity<43:
  hpo1 = KitronikHighPowerOut(1)
elif humidity>47:
  hpo2 = KitronikHighPowerOut(2)
else:
  
