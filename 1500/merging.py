#!/usr/bin/python -i

from tkinter import *
from tkinter import ttk # need this for tabs and notebook widget
from time import sleep
import threading
import RPi.GPIO as GPIO
import piplates.RELAYplate as RELAY

### setup GPIO mode
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

### create GUI window
window = Tk()
window.title("1500 Cycle Tester")
window.geometry('400x400')
style=ttk.Style(window) # sets the theme for the gui
style.theme_use("default")
notebook = ttk.Notebook(window)

tab1 = Frame(notebook)
tab2 = Frame(notebook)

notebook.add(tab1,text="Cycler")
notebook.add(tab2,text="Setup")
notebook.pack(expand = 1, fill = "both")  
                                      
### input variables from GUI
combo1 = 0
combo2 = 0
combo3 = 0
cyclesint = IntVar()
cycles = 0
cycles_completed = 0
cycle_keeper = 0

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
    global cycles, cycles_completed, cycle_keeper
    #cyclehelper = "Cycles Remaining : 0"
    #cyclesremaininglable.configure(text = cyclehelper)
    cycles_completed = cyclesInitial - cycle_keeper
    reporthelper = "Actual Complete Cycles: " + str(cycles_completed)
    report1lable.configure(text = reporthelper)
    # print("Cycles requested: ", cyclesInitial)
    # print("Shackle failed to open ", shackle_not_open_count, " times")
    # print("Shackle failed to lock ", shackle_not_locked_count, " times")
    # print("Shackle failed to close ", shackle_not_closed_count, " times")
    # print("Actual complete cycles: ", cyclesInitial - (cycles))
    # print("Cycles remaining when stopped: ", cycles)
    RELAY.relayOFF(0,unlock_shackle_pin)
    RELAY.relayOFF(0,lock_shackle_pin)
    #input("Press enter to exit")
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
    global shackle_not_open_count,shackle_not_open_helper, direction, cycles
    if shackle_not_open_count >= 350 or cycles <= 0:
        #print("erorr with shackle not opening")
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
    if shackle_not_locked_count >= 25:
        print("erorr with shackle not locking")
        program_end()
    if GPIO.input(open_switch) == True:
        shackle_not_locked_count += 1
        #cycles += 1
        print("Shackle failed to lock ", shackle_not_locked_count, " times")
        push_shackle_closed()
        shackle_lock_check()
    # if shackle_not_locked_count >= 25:
    #     print("erorr with shackle not locking")
    #     program_end()

### GUI LAYOUT ###
combo1label = Label(tab1, text="Combo 1")
combo1label.grid(column=0, row=0, sticky=E, padx=(10,30))

combo2label = Label(tab1, text="Combo 2")
combo2label.grid(column=0, row=1, sticky=E, padx=(10,30))

combo3label = Label(tab1, text="Combo 3")
combo3label.grid(column=0, row=2, sticky=E, padx=(10,30))

combo1txt = Entry(tab1,width=10, highlightthickness=0)
combo1txt.grid(column=1, row=0)

combo2txt = Entry(tab1,width=10, highlightthickness=0)
combo2txt.grid(column=1, row=1)

combo3txt = Entry(tab1,width=10, highlightthickness=0)
combo3txt.grid(column=1, row=2)

cycleslabel = Label(tab1, text="Number of Cycles")
cycleslabel.grid(column=0, row=3, sticky=E, padx=(10,30))

cyclestxt = Entry(tab1,width=10, highlightthickness=0)
cyclestxt.grid(column=1, row=3)

joglabel = Label(tab2, text="Jog Increments")
joglabel.grid(column=0, row=11, sticky=E, padx=(60,0))

jogtxt = Entry(tab2,width=8, highlightthickness=0)
jogtxt.grid(column=1, row=11, sticky=EW, padx=(20,20))

currentinfo = Label(tab1, text="Cycles Requested    ")
currentinfo.grid(column=0, row=7, columnspan = 2, sticky=W, padx=(10,30))

cyclesremaininglable = Label(tab1, text="Cycles Remaining    ")
cyclesremaininglable.grid(column=0, row=8, columnspan = 2, sticky=W, padx=(10,30))

report1lable = Label(tab1, text="Actual Complete Cycles    ")
report1lable.grid(column=0, row=9, columnspan = 2, sticky=W, padx=(10,30))

dividerlineupper = Label(tab1, text="    ____________________________")
dividerlineupper.grid(column=0, row=6, columnspan = 2, sticky=EW, pady=(20,20))


def main():
    global cycles, cyclesint, direction, cycle_keeper
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

        push_shackle_closed()

        sleep(shacklePause)
        sleep(.1)
        #cycles -= 1

        cyclehelper = "Cycles Remaining : " + str(cycles)
        cyclesremaininglable.configure(text = cyclehelper)
        requestedhelper = "Cycles Requested: " + str(cyclesInitial)
        currentinfo.configure(text= requestedhelper)
        cycles_completed = cyclesInitial - cycles
        reporthelper = "Actual Complete Cycles: " + str(cycles_completed)
        report1lable.configure(text = reporthelper)
        
        cycles -= 1
        sleep(.25)

    program_end()

# this function sets all the program variables to the user inputs from the GUI
def start_program():
    global cycles, cyclesint, combo1, combo2, combo3, distanceToZero, cyclesInitial, cycles_completed
    cycles= int(cyclestxt.get())
    combo1 = int(combo1txt.get())
    combo2 = int(combo2txt.get())
    combo3 = int(combo3txt.get())
    distanceToZero = 40 - combo3
    cyclesInitial = cycles
    main()

def relay_reset():
    print("turn off relays")
    RELAY.relayOFF(0,1)
    RELAY.relayOFF(0,2)
    RELAY.relayOFF(0,3)
    RELAY.relayOFF(0,4)
    RELAY.relayOFF(0,5)
    RELAY.relayOFF(0,6)
    RELAY.relayOFF(0,7)

def stop_program():
    #print("Stop Program")
    global cycles, cycles_completed, cycle_keeper
    cycle_keeper = cycles
    #cyclehelper = "Cycles Remaining : 0"
    #cyclesremaininglable.configure(text = cyclehelper)
    cycles= -1
    program_end()

def jog_func():
    jog_helper = int(jogtxt.get())
    motor_turns(jog_helper)

def jogstep_func():
    GPIO.output(direction_pin, direction)
    RELAY.relayON(0,lock_shackle_pin)
    sleep(shacklePause)
    sleep(shacklePause)
    RELAY.relayOFF(0,lock_shackle_pin)
    global pulse
    for i in range(2):
        GPIO.output(pulse_pin, pulse)
        sleep(motorSpeed)
        pulse = not pulse # changes pulse pin from high to low each time through loop


### GUI BUTTONS ###
startbutton = Button(tab1, text="Start", bg = 'green',highlightthickness=2, command=threading.Thread(target=start_program).start, width=10)
startbutton.grid(column=0, row=4)

stop = Button(tab1, text="Stop", bg = 'red', highlightthickness=2, command=threading.Thread(target=stop_program).start, width=10)
stop.grid(column=1, row=4)

relaysoff = Button(tab2, text="Relays Off", highlightthickness=2, command=relay_reset, width=10)
relaysoff.grid(column=0, row=12, sticky=E)

jogbutton = Button(tab2, text="Jog Dial", highlightthickness=2, command=jog_func, width=10)
jogbutton.grid(column=1, row=12, sticky=W)

jogbuttonstep = Button(tab2, text="Half Step", highlightthickness=2, command=jogstep_func, width=10)
jogbuttonstep.grid(column=1, row=13, sticky=W)

window.mainloop()

#if __name__ == '__main__':
#   main()
GPIO.cleanup() # clear GPIO allocations after running program