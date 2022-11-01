from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)
open_valve = Pin(0, Pin.OUT)
close_valve = Pin(1, Pin.OUT)
open_switch = Pin(2, Pin.IN, Pin.PULL_DOWN)
cycles = int(input("Number of cycles: "))


pull_door():
    while open_switch.value() == False:
        open_valve.on()
        led.on()
        print("open valve")
        
push_door():
    if open_switch.value() == False:
        pull_door()
    elif open_switch.value() == True:
        close_valve.on()
        sleep(5)
        close_valve.off()
main():
    while cycles > 0:
        print(open_switch.value())
        pull_door()
        push_door()
        cycles -= 1