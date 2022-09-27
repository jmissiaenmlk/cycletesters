import RPi.GPIO as GPIO
import time
# JDP:  the other way
# from time import sleep
from gpiozero import Button


# JDP: next time I am in lets review everything below this until def motor1cal().  It would make sense to move some of this around to help make the code more modular.
#      I'd rather review this part in person to explain it in better detail.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# define GPIO pins motor 1
direction = 22  # Direction (DIR) GPIO Pin
step = 20  # Step GPIO Pin
EN_pin = 24  # enable pin (LOW to enable)

# define GPIO pins motor 2
directionpin2 = 7  # Direction (DIR) GPIO Pin
step2 = 16  # Step GPIO Pin
EN_pin2 = 23  # enable pin (LOW to enable)

limswitch_fwd = Button(12, pull_up=False)
torque_limit = Button(13, pull_up=False)
push_pull_limit = Button(17, pull_up=False)

travel = 9100  # motor 1 steps for linear travel // .0002" linear travel per pulse
travel2 = 400  # motor 2 steps for key turn
pulse = False  # JJM
direction1 = False  # False = reverse
direction2 = True
cycles = int(input("Enter Number of Cycles:"))
cyclesstart = cycles

# motor 1 enable setup and ouput
GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output
GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
# motor 2 enable setup and ouput
GPIO.setup(EN_pin2, GPIO.OUT)  # set enable pin as output
GPIO.output(EN_pin2, GPIO.LOW)  # pull enable to low to enable motor


def motor1cal():  # calibration so linear motor knows where it is in relation to key cylinder
    global travel, pulse, direction1, cycles  # JJM
    # JDP: I would rename the direction variables to is_direction_fwd or something like that to help clarify what True/False means
    direction1 = True
    # JDP: Changed while limswitch_fwd.is_pressed == False: to simplify the expression
    #      what you had was valid, but this makes it easier to understand at a glance.
    while not limswitch_fwd.is_pressed:
        pulse = not pulse  # JJM
        motor1()
        time.sleep(.0002)  # JDP: If your lazy like me, you can import sleep differently so that you don't have to type the time.
                           # you may not have learned this yet, I have the other way commented out at the top by the imports


def motor1end():
    global travel, pulse, direction1, cycles  # JJM
    travel = 18000
    direction1 = False
    for x in range(travel):  # JJM
        pulse = not pulse  # JJM
        motor1()
        time.sleep(.0002)
    print("Done!", cyclesstart, " Cycles completed")


def motor1fwd():
    global travel, pulse, direction1, cycles  # JJM

    direction1 = True
    for z in range(2):
        direction1 = not direction1
        for x in range(travel):  # JJM
            pulse = not pulse  # JJM
            motor1()
            time.sleep(.00001)
    else:
        # JDP: I would move the Cycles remaining message and the cycles decrement
        #      as it you will see a Cycles remaining -1 message at the end
        cycles -= 1
        print("Cycles remaining: ", cycles)
        motor2fwd()


def motor2fwd():
    global pulse, direction2, cycles  # JJM
    for y in range(2):
        direction2 = not direction2  # JJM
        for x in range(travel2):  # JJM
            pulse = not pulse
            # JJM
            motor2()
            time.sleep(.001)
        
def motor1():
    GPIO.setup(step, GPIO.OUT)
    GPIO.setup(direction, GPIO.OUT)
    GPIO.output(step, pulse)  # toggle is the same a pulse/step
    GPIO.output(direction, direction1)  # LOW = CCW, HIGH = CW


def motor2():
    GPIO.setup(step2, GPIO.OUT)
    GPIO.setup(directionpin2, GPIO.OUT)
    GPIO.output(step2, pulse)  # toggle is the same a pulse/step
    GPIO.output(directionpin2, direction2)  # LOW = CCW, HIGH = CW

def torquelimit():
    global tlim, flim
    
    tlim = True
    print ("Torque Limit Reached")
    print("tlim ", tlim, "flim ", flim)
  
        
    
def pushpulllimit():
    global flim, tlim
    
    flim = True
    tlim = False
    print ("Push/Pull Limit Reached")
    print("tlim ", tlim, "flim ", flim)

    
torque_limit.when_pressed = torquelimit
push_pull_limit.when_pressed = pushpulllimit
tlim = False
flim = False
# 
# motor1cal()
# 
# input("Press enter when ready")
# while cycles > 0:
#     if tlim == False:
#         motor1fwd()
#     else:
#         input("enter key to cont")
# else:
#    input("any key to cont")
def main():
    motor1cal()

    # JDP: moved this here to make it easier for someone new looking at the code or for your future self to determine where the main logic starts
    input("Press Enter When Ready")
    while cycles > 0:
        motor1fwd()
    
    motor1end()

    GPIO.cleanup()  # clear GPIO allocations after run


# JDP: This wierd looking if statement is the entry point if you run the .py directly.  By doing it this way you can expose functions in the file for
#      use elsewhere or run it on its own.
if __name__ == '__main__':
    main()
