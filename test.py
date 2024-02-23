from time import sleep
from KitronikAirQualityControlHAT import *
import RPi.GPIO as gpio
bme688 = KitronikBME688()
oled = KitronikOLED()
hpo1 = KitronikHighPowerOut(1)
hpo2 = KitronikHighPowerOut(2)
buzzer = KitronikBuzzer()

bme688.calcBaselines(oled)
bme688.measureData()
# Read and output the sensor values
print("Temperature:", bme688.readTemperature())
print("Pressure:", bme688.readPressure())
print("Humidity:", bme688.readHumidity())
print("eCO2:", bme688.readeCO2())
print("Air Quality %:", bme688.getAirQualityPercent())
print("Air Quality Score:", bme688.getAirQualityScore())