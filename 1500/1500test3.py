# JJM 9/27/2021 for 1500 combo lock cycle tester

from time import sleep
import RPi.GPIO as GPIO
import piplates.RELAYplate as RELAY

# setup GPIO mode
GPIO.setmode(GPIO.BCM)


code1 = int((input("Enter first number ")))
code2 = int((input("Enter second number ")))
code3 = int((input("Enter third number ")))
cycles = int((input("Enter number of cycles ")))
currentPosition = 0
distanceToZero = 40 - code3
pulse = False # pulses pin high and low to create a step
direction = True # true = CW 

# setup GPIO pins
GPIO.setup(19, GPIO.OUT) # step /pulse pin 19
GPIO.setup(26, GPIO.OUT) # direction pin 26
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # limit switch

def motorTurns(pos1):
    GPIO.output(26, direction)
    global pulse, currentPosition
    for i in range(pos1*20):
        GPIO.output(19, pulse)
        sleep(.0005)
        pulse = not pulse
    currentPosition = pos1


while cycles > 0:
    motorTurns(40 + (40-code1))
    print("Code 1")
    sleep(1)
    direction = not direction
    if code2 > code1:
        motorTurns(40 + (code2 - code1))
        print("Code to > code 1")
        sleep(1)
        direction = not direction
    elif code2 < code1:
        motorTurns(40 + (40 - code1 + code2))
        print("Code2 < code1")
        sleep(1)
        direction = not direction
    if code3 > code2:
        motorTurns(40 - code3 + code2)
        print("code3 > code2")
        sleep(1)
        direction = not direction
    elif code3 < code2:
        motorTurns(code2 - code3)
        print("Code3 < code2")
        sleep(1)
        direction = not direction
    sleep(.50)
    RELAY.relayON(0,7)
    sleep(.50)
    RELAY.relayOFF(0,7)
    sleep(1)
    motorTurns(distanceToZero)
    sleep(1)
    RELAY.relayON(0,6)
    sleep(.50)
    RELAY.relayOFF(0,6)
    sleep(.50)
    print("Return to 0")

    direction = not direction
    sleep(1)
    cycles -= 1