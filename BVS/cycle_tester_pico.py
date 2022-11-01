from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)
open_valve = Pin(0, Pin.OUT, value = 1)
close_valve = Pin(1, Pin.OUT, value = 0)
opened_switch = Pin(2, Pin.IN, Pin.PULL_DOWN)
closed_switch = Pin(3, Pin.IN, Pin.PULL_DOWN)
cycles = int(input("Number of cycles: "))
time_delay = .25

def pull_door():
    if opened_switch.value() == True and closed_switch.value() == False:
        print("door was opened")
        sleep(time_delay)
    else:
        while opened_switch.value() == False:
            open_valve.on()
            print("open valve")
            sleep(time_delay)
            open_valve.off()
        
def push_door():
    if closed_switch.value() == True and opened_switch.value() == False:
        print("door was closed")
        sleep(time_delay)
    else:
        while closed_switch.value() == False:
            close_valve.on()
            print("push door")
            sleep(time_delay)
            close_valve.off()
            
        
def main():
    global cycles
    while cycles > 0:
        pull_door()
        push_door()
        cycles -= 1
        print("Number of cycles remaining: ", cycles)
        sleep(time_delay)

if __name__ == '__main__':
    main()


