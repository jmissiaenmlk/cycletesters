#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from math import pow
import piplates.RELAYplate as RELAY


##  Setting pin modes
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


class App:
    
    def pulseMotor(pulsePin, dirPin, direction, deg, velocity):
        pulseRev = 100 ##  Pulses per revolution
        pulses = (deg * 10)##  Number of pulses for desired travel
        psec = (pow(10.0,6)) / (1000 * (pulseRev / 360.0)) ##  number of pulses/sec for desired speed
        currentDirection = GPIO.input(dirPin) ##  Checking current direction
        if (direction != currentDirection):
            GPIO.output(dirPin, direction)
            time.sleep(0.01)
            
        ##  Loop for pulsing the drive
        for p in range(0, int(pulses)):
        ##    //the LOW, then HIGH creates the pulse the driver is waiting for.
            GPIO.output(pulsePin, GPIO.LOW)
            time.sleep(.00175)
            GPIO.output(pulsePin, GPIO.HIGH)
            time.sleep(.000001)
        
    
    ##  End function declaration
            
    motor1Speed = 360 ##  deg/sec
    motor1Travel = int(input("Travel to combo 1: "))
    motor2Travel = int(input("Travel to combo 2: "))
    motor3Travel = int(input("Travel to combo 3: "))
    motor4Travel = int(input("Travel to zero: "))
   
    cycle = int(input("Enter Number Of Cycles: "))
    fail = 0
    failtest = 0

    while cycle >= 0:
        print("cycle",cycle)
        pulseMotor(19, 26, True, motor1Travel, motor1Speed)
        time.sleep(1)
        pulseMotor(19, 26, False, motor2Travel, motor1Speed)
        time.sleep(1)
        pulseMotor(19, 26, True, motor3Travel, motor1Speed)
        time.sleep(1)
        RELAY.relayON(0,6)
        time.sleep(.50)
        RELAY.relayOFF(0,6)
        time.sleep(.50)
        if GPIO.input(4):
             print("shackle open")
             print("Failed Cycles: ",fail)
        else:
             fail +=1
             print("shackle close",fail)
             if fail==10 :
                  print("Stoped at Cycle: ",cycle)
                  break
        time.sleep(.50)
        RELAY.relayON(0,7)
        time.sleep(.50)
        RELAY.relayOFF(0,7)
        time.sleep(1)
        pulseMotor(19, 26, True, motor4Travel, motor1Speed)
        time.sleep(1)
        RELAY.relayON(0,6)
        time.sleep(.50)
        RELAY.relayOFF(0,6)
        time.sleep(.50)
        if GPIO.input(4):
             failtest +=1
             print("Fail Shackle Test close")
             if failtest==2 :
                  print("Stoped at Cycle: ",cycle)
                  print("Test Failed Cycles", failtest)
                  break
        else:
             print("Pass Shackle Test Open")
             print("Test Failed Cycles: ",failtest)
             
        time.sleep(.50)
        RELAY.relayON(0,7)
        time.sleep(.50)
        RELAY.relayOFF(0,7)
        time.sleep(1)
        cycle-=1
     
    close = input("close screen and re-open to restart")