import pcf8574
from machine import I2C, Pin
from time import sleep

# TinyPICO (ESP32)
i2c = I2C(1,scl=Pin(7), sda=Pin(6))
pcf = pcf8574.PCF8574(i2c, 0x27)

# # read pin 2
# pcf.pin(3)
# 
# # set pin 3 HIGH
# pcf.pin(3, 1)
# 
# # set pin 4 LOW
# pcf.pin(4, 0)
# 
# # toggle pin 5
# pcf.toggle(5)
# 
# # set all pins at once with 8-bit int
# pcf.port = 0xff
# 
# # read all pins at once as 8-bit int
# pcf.port

while True:
    pcf.toggle(0)
    sleep(.1)
    pcf.toggle(1)
    sleep(.1)
    pcf.toggle(2)
    sleep(.1)
    pcf.toggle(3)
    pcf.toggle(4)
    sleep(.1)
    pcf.toggle(5)
    sleep(.1)
    pcf.toggle(6)
    pcf.toggle(7)
    pcf.toggle(7)
    sleep(.1)
    pcf.toggle(6)
    sleep(.1)
    pcf.toggle(5)
    sleep(.1)
    pcf.toggle(4)
    pcf.toggle(3)
    sleep(.1)
    pcf.toggle(2)
    sleep(.1)
    pcf.toggle(1)
    pcf.toggle(0)
    sleep(.2)
    pcf.toggle(4)
    sleep(.5)
    pcf.toggle(4)
    sleep(.5)
    pcf.toggle(7)
    sleep(.8)
    pcf.toggle(2)
    sleep(.8)
    pcf.toggle(1)
    sleep(.8)