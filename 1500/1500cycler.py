# JJM 9/27/2022 for 1500 combo lock cycle tester
# use this line at the top of the code to run  in terminal #!/usr/bin/python -i

from time import sleep
import RPi.GPIO as GPIO
import piplates.RELAYplate as RELAY

# setup GPIO mode
GPIO.setmode(GPIO.BCM)

combo1 = int((input("Enter first combination number ")))
combo2 = int((input("Enter second combination number ")))
combo3 = int((input("Enter third combination number ")))
cycles = int((input("Enter number of cycles ")))
##################### these variables control speed of the various functions
motorSpeed = .0004  #
dialPause = .2      #
shacklePause = .35  #
#####################
cyclesInitial = cycles # keeps original cycle count
distanceToZero = 40 - combo3
pulse = False # pulses pin high and low to create a step
direction = True # true = CW 
shackleNotOpenCount = 0
shackleNotLockedCount = 0
shackle_failed_open = 0
# setup GPIO pins
GPIO.setup(19, GPIO.OUT) # step /pulse pin 19
GPIO.setup(26, GPIO.OUT) # direction pin 26
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # shackle open switch
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # shackle close switch
open_switch = 4 # input pin
close_switch = 5 # input pin
lock_shackle_pin = 5 # output pin
unlock_shackle_pin = 7 # output pin


def motorTurns(x): # passes info from main loop about combinations into function to turn dial
    GPIO.output(26, direction)
    global pulse, currentPosition
    for i in range(x*20):
        GPIO.output(19, pulse)
        sleep(motorSpeed)
        pulse = not pulse # changes pulse pin from high to low each time through loop


while cycles > 0:
    # cycle starts by spinning combo dial 2 rotations before dialing in combo 1
    motorTurns(120 + (40-combo1))
    sleep(dialPause)
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
    RELAY.relayON(0,unlock_shackle_pin) # pull shackle open / unlock shackle
    sleep(shacklePause)
    RELAY.relayOFF(0,unlock_shackle_pin)
    sleep(shacklePause)
    shackle_failed_open = 0

    if GPIO.input(open_switch) == False: # checks to see if shackle opened
        shackleNotOpenCount += 1
        cycles += 1
        print("Shackle Failed to unlock ",shackleNotOpenCount, " times")
        if shackleNotOpenCount == 25:
            break

    RELAY.relayON(0,lock_shackle_pin) # push shackle closed / lock shackle
    sleep(shacklePause)
    RELAY.relayOFF(0,lock_shackle_pin)
    sleep(shacklePause)
    sleep(shacklePause)
    motorTurns(distanceToZero) # spins dial back to 0 to keep position info
    direction = not direction
    motorTurns(40)
    direction = not direction # spins dial around to make sure combo is scrambled
    sleep(shacklePause)
    RELAY.relayON(0,unlock_shackle_pin) # pull shackle open to test if it locked correctly
    sleep(shacklePause)
    RELAY.relayOFF(0,unlock_shackle_pin)
    sleep(shacklePause)
    if GPIO.input(open_switch) == True:
        shackleNotLockedCount += 1
        cycles += 1
        print("Shackle failed to lock ", shackleNotLockedCount, " times")
        if shackleNotLockedCount == 25:
            break

    RELAY.relayON(0,lock_shackle_pin) # push shackle closed
    sleep(shacklePause)
    RELAY.relayOFF(0,lock_shackle_pin)
    sleep(shacklePause)
    sleep(shacklePause)
    direction = not direction
    sleep(.1)
    cycles -= 1
    print("cycles remaining ", cycles)

print("Cycles requested: ", cyclesInitial)
print("Shackle failed to open ", shackleNotOpenCount, " times")
print("Shackle failed to lock ", shackleNotLockedCount, " times")
print("Actual complete cycles: ", cyclesInitial - (cycles))
print("Cycles remaining when stopped: ", cycles)
RELAY.relayOFF(0,unlock_shackle_pin)
RELAY.relayOFF(0,lock_shackle_pin)
GPIO.cleanup() # clear GPIO allocations after running program

input("End of cycle. Press Enter")
input("Press enter to exit")