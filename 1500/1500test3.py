# JJM 9/27/2021 for 1500 combo lock cycle tester

from time import sleep
import RPi.GPIO as GPIO
import piplates.RELAYplate as RELAY

# setup GPIO mode
GPIO.setmode(GPIO.BCM)

combo1 = int((input("Enter first combination number ")))
combo2 = int((input("Enter second combination number ")))
combo3 = int((input("Enter third combination number ")))
cycles = int((input("Enter number of cycles ")))
# these variables control speed of the various functions
motorSpeed = .0002
dialPause = .2
shacklePause = .5

distanceToZero = 40 - combo3
pulse = False # pulses pin high and low to create a step
direction = True # true = CW 

# setup GPIO pins
GPIO.setup(19, GPIO.OUT) # step /pulse pin 19
GPIO.setup(26, GPIO.OUT) # direction pin 26
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # limit switch

def motorTurns(self): # passes info from main loop about combinations into function to turn dial
    GPIO.output(26, direction)
    global pulse, currentPosition
    for i in range(self*20):
        GPIO.output(19, pulse)
        sleep(motorSpeed)
        pulse = not pulse # changes pulse pin from high to low each time through loop


while cycles > 0:
    # cycle starts by spinning combo dial 2 rotations before dialing in combo 1
    motorTurns(80 + (40-combo1))
    sleep(1)
    direction = not direction
    if combo2 > combo1:
        motorTurns(40 + (combo2 - combo1))
        sleep(dialPause)
        direction = not direction
    elif combo2 < combo1:
        motorTurns(40 + (40 - combo1 + combo2))
        sleep(dialPause)
        direction = not direction
    if combo3 > combo2:
        motorTurns(40 - combo3 + combo2)
        sleep(dialPause)
        direction = not direction
    elif combo3 < combo2:
        motorTurns(combo2 - combo3)
        sleep(dialPause)
        direction = not direction
    sleep(shacklePause)
    RELAY.relayON(0,7) # pull shackle open
    sleep(shacklePause)
    RELAY.relayOFF(0,7)
    sleep(shacklePause)
    RELAY.relayON(0,6) # push shackle closed
    sleep(shacklePause)
    RELAY.relayOFF(0,6)
    sleep(shacklePause)
    motorTurns(distanceToZero)
    direction = not direction
    sleep(1)
    cycles -= 1
    print("cycles remaining ", cycles)