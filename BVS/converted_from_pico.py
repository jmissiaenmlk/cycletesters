# JJM 11/1/2022 for BVS door cycle tester
# use this line at the top of the code to run  in terminal #!/usr/bin/python -i

from time import sleep
import RPi.GPIO as GPIO
import piplates.RELAYplate as RELAY

# setup GPIO mode
GPIO.setmode(GPIO.BCM)

### setup GPIO pins ###
GPIO.setup(19, GPIO.OUT) # step /pulse pin 19
GPIO.setup(26, GPIO.OUT) # direction pin 26
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # shackle open switch
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # shackle close switch
### --------------- ###

### IO pin variables ###
open_switch = 4 # input pin
close_switch = 27 # input pin
lock_shackle_pin = 5 # output pin
unlock_shackle_pin = 7 # output pin

cycles = 0
time_delay = .25

def pull_door():
    if GPIO.input(open_switch) == True and GPIO.input(close_switch) == False:
        print("door was opened")
        sleep(time_delay)
    else:
        while GPIO.input(open_switch) == False:
            RELAY.relayON(0,unlock_shackle_pin)
            print("open valve")
            sleep(time_delay)
            RELAY.relayOFF(0,unlock_shackle_pin)
        
def push_door():
    if GPIO.input(close_switch) == True and GPIO.input(open_switch) == False:
        print("door was closed")
        sleep(time_delay)
    else:
        while GPIO.input(close_switch) == False:
            RELAY.relayON(0,lock_shackle_pin)
            print("push door")
            sleep(time_delay)
            RELAY.relayOFF(0,lock_shackle_pin)
            
        
def main():
    global cycles, cycles_start
    cycles_start = cycles
    while cycles > 0:
        pull_door()
        push_door()
        cycles -= 1
        print("Number of cycles remaining: ", cycles)
        sleep(time_delay)

