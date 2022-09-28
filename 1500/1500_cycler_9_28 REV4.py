# EDS 9/27/2021 for 1500 combo lock cycle tester

from time import sleep
import RPi.GPIO as GPIO
import piplates.RELAYplate as RELAY

# setup GPIO mode
GPIO.setmode(GPIO.BCM)

code1 = int((input("Enter first code number: ")))
code2 = int((input("Enter second code number: ")))
code3 = int((input("Enter third code number: ")))
cycles = int((input("Enter desired number of cycles: ")))
currentPosition = 0
CW = -1
CCW = 1

distanceToZero = 40 - code3
pulse = False # pulses pin high and low to create a step
#direction = True # true = CW 

# setup GPIO pins
GPIO.setup(19, GPIO.OUT) # step /pulse pin 19
GPIO.setup(26, GPIO.OUT) # direction pin 26
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # limit switch

def motorMove(targetNumber, direction):
    GPIO.output(26, direction)
    global currentPosition, pulse
    
    if direction == CW:
        GPIO.output(26, True)
        incrementVal = -1
    elif direction == CCW:
        GPIO.output(26, False)
        incrementVal = 1
    
    if currentPosition == targetNumber:
        print('Single Increment: ', currentPosition)
        for i in range(20):
            GPIO.output(19, pulse)
            sleep(.001)
            pulse = not pulse
        currentPosition = currentPosition + incrementVal
        
    while currentPosition != targetNumber:
        print('Looped Increment: ', currentPosition)
        for i in range(20):
            GPIO.output(19, pulse)
            sleep(.001)
            pulse = not pulse 
        currentPosition = currentPosition + incrementVal
        if currentPosition == -1:
            currentPosition = 39
        if currentPosition == 40:
            currentPosition = 0

while cycles > 0:
    motorMove(0, CW) #full CW turn at zero to clear previous codes
    motorMove(0, CW) #full CW turn at zero to clear previous codes
    motorMove(0, CW) #full CW turn at zero to clear previous codes
    motorMove(code1, CW) #turn CW to first code position
    motorMove(code2, CCW) #turn CCW to second code position
    motorMove(code2, CCW) #full turn CCW at second code position
    motorMove(code3, CW) #turn CW to third code

    sleep(.50)
    RELAY.relayON(0,7)
    sleep(.50)
    RELAY.relayOFF(0,7)
    sleep(1)
    RELAY.relayON(0,6)
    sleep(.50)
    RELAY.relayOFF(0,6)
    sleep(.50)
    print("Return to 0")

    sleep(1)
    cycles -= 1