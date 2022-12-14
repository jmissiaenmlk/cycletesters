# JJM 10/6/2022 for 1500 combo lock cycle tester
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
direction_pin = 26 # output pin that controls motor direction
pulse_pin = 19 # ouput pin that controls motor pulses
### ---------------- ###

### input variables ###
combo1 = int((input("Enter first combination number ")))
combo2 = int((input("Enter second combination number ")))
combo3 = int((input("Enter third combination number ")))
cycles = int((input("Enter number of cycles ")))
### --------------- ###

### general variables ###
cyclesInitial = cycles # keeps original cycle count
distanceToZero = 40 - combo3
pulse = False # pulses pin high and low to create a step
direction = True # true = CW 
shackle_not_open_count = 0
shackle_not_open_helper = 0
shackle_not_locked_count = 0
shackle_not_closed_count = 0
shackle_failed_open = 0
### ----------------- ###

### these variables control speed of the various functions ###
motorSpeed = .0004    #
dialPause = .2        #
shacklePause = .35    # 
short_pause = .1      #
### --------------- ###

# passes info from main loop about combinations into function to turn dial
def motor_turns(x): 
    GPIO.output(direction_pin, direction)
    RELAY.relayON(0,lock_shackle_pin)
    sleep(shacklePause)
    sleep(shacklePause)
    RELAY.relayOFF(0,lock_shackle_pin)
    global pulse
    for i in range(x*20):
        GPIO.output(pulse_pin, pulse)
        sleep(motorSpeed)
        pulse = not pulse # changes pulse pin from high to low each time through loop

def program_start():
    global direction
    motor_turns(120 + (40-combo1))
    sleep(dialPause)
    direction = not direction
    if combo2 > combo1:
        motor_turns(40 + (combo2 - combo1))
        sleep(dialPause)
        direction = not direction
    elif combo2 < combo1:
        motor_turns(40 + (40 - combo1 + combo2))
        sleep(dialPause)
        direction = not direction
    if combo3 > combo2:
        motor_turns(40 - combo3 + combo2)
        sleep(dialPause)
        direction = not direction
    elif combo3 < combo2:
        motor_turns(combo2 - combo3)
        sleep(dialPause)
        direction = not direction

# various info printed at end of program as well as cleaning up GPIO
def program_end():
    global cycles
    print("Cycles requested: ", cyclesInitial)
    print("Shackle failed to open ", shackle_not_open_count, " times")
    print("Shackle failed to lock ", shackle_not_locked_count, " times")
    print("Shackle failed to close ", shackle_not_closed_count, " times")
    print("Actual complete cycles: ", cyclesInitial - (cycles))
    print("Cycles remaining when stopped: ", cycles)
    RELAY.relayOFF(0,unlock_shackle_pin)
    RELAY.relayOFF(0,lock_shackle_pin)
    input("Press enter to exit")
    exit()
    

# pulls shackle open
def pull_shackle_open():
    RELAY.relayOFF(0,lock_shackle_pin) # makes sure lock shackle relay is off
    RELAY.relayON(0,unlock_shackle_pin) # pull shackle open / unlock shackle
    sleep(short_pause)
    RELAY.relayOFF(0,unlock_shackle_pin)
    sleep(short_pause)
    RELAY.relayON(0,lock_shackle_pin) # pull shackle open / unlock shackle
    sleep(.05)
    RELAY.relayOFF(0,lock_shackle_pin)
    sleep(.01)
    RELAY.relayON(0,unlock_shackle_pin) # pull shackle open / unlock shackle
    sleep(shacklePause)
    RELAY.relayOFF(0,unlock_shackle_pin)
    sleep(shacklePause)

# checks to see if shackle opened and will pull the shackle again if it didn't open on the 1st try
def shackle_open_check():
    global shackle_not_open_count,shackle_not_open_helper, direction
    if shackle_not_open_count >= 350:
        print("erorr with shackle not opening")
        program_end()
    elif shackle_not_open_helper == 4:
        push_shackle_closed()
        motor_turns(distanceToZero) # spins dial back to 0 to keep position info
        direction = not direction
        print("Redial Combo")
        program_start()
        pull_shackle_open()
        shackle_not_open_helper = 0
        shackle_open_check()
    elif GPIO.input(open_switch) == False: # checks to see if shackle opened
        shackle_not_open_count += 1
        shackle_not_open_helper += 1
        #print("Shackle Failed to unlock ",shackle_not_open_count, " times")
        pull_shackle_open()
        shackle_open_check()
    elif GPIO.input(open_switch) == True: # checks to see if shackle opened
        # print("Shackle Opened")
        return ("shackle opened")


# push shackle closed / lock shackle
def push_shackle_closed():
    global shackle_not_closed_count
    RELAY.relayOFF(0,unlock_shackle_pin) # makes sure unlock shackle relay is off
    RELAY.relayON(0,lock_shackle_pin)
    sleep(shacklePause)
    RELAY.relayOFF(0,lock_shackle_pin)
    sleep(shacklePause)
    if shackle_not_closed_count >= 25:
        print("erorr with shackle not closing")
        program_end()
    elif GPIO.input(close_switch) == False:
        shackle_not_closed_count += 1
        push_shackle_closed()      

# pull shackle open to test if it locked correctly
def shackle_lock_check():
    global cycles, shackle_not_locked_count
    RELAY.relayON(0,unlock_shackle_pin)
    sleep(shacklePause)
    RELAY.relayOFF(0,unlock_shackle_pin)
    sleep(shacklePause)
    if GPIO.input(open_switch) == True:
        shackle_not_locked_count += 1
        cycles += 1
        print("Shackle failed to lock ", shackle_not_locked_count, " times")
    if shackle_not_locked_count == 25:
        print("erorr with shackle not locking")
        program_end()

def main():
    global cycles, direction
    while cycles > 0:
        RELAY.relayOFF(0,1)
        RELAY.relayOFF(0,2)
        RELAY.relayOFF(0,3)
        RELAY.relayOFF(0,4)
        RELAY.relayOFF(0,6)
        # cycle starts by spinning combo dial 2 rotations before dialing in combo 1
        program_start()

        sleep(shacklePause)

        pull_shackle_open()

        shackle_open_check()

        push_shackle_closed()

        shackle_lock_check()

        sleep(shacklePause)
        motor_turns(distanceToZero) # spins dial back to 0 to keep position info
        direction = not direction
        
        #motor_turns(40)
        #direction = not direction # spins dial around to make sure combo is scrambled
        #sleep(shacklePause)

        #shackle_lock_check()

        push_shackle_closed()

        sleep(shacklePause)
        #direction = not direction
        sleep(.1)
        cycles -= 1
        print("cycles remaining ", cycles)

    program_end()

    input("End of cycle. Press Enter")
    input("Press enter to exit")

if __name__ == '__main__':
    main()
GPIO.cleanup() # clear GPIO allocations after running program