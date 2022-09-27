import RPi.GPIO as GPIO
from time import sleep
from gpiozero import Button

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# define GPIO pins motor 1
direction_pin_m1 = 22  # Direction (DIR) GPIO Pin
step_pin_m1 = 20  # Step GPIO Pin
EN_pin_m1 = 24  # enable pin (LOW to enable)

# define GPIO pins motor 2
direction_pin_m2 = 7  # Direction (DIR) GPIO Pin
step_pin_m2 = 16  # Step GPIO Pin
EN_pin_m2 = 23  # enable pin (LOW to enable)

limitswitch_m1_fwd = Button(12, pull_up=False)
limitswitch_m1_rev = Button(13, pull_up=False)

travel_m1 = 9100  # motor 1 steps for linear travel // .0002" linear travel per pulse
travel_m2 = 400  # motor 2 steps for key turn
pulse = False  # JJM
direction_m1 = False  # False = reverse
direction_m2 = True
cycles = int(input("Enter Number of Cycles:"))
cyclesstart = cycles

# motor 1 enable setup and ouput
GPIO.setup(EN_pin_m1, GPIO.OUT)  # set enable pin as output
GPIO.output(EN_pin_m1, GPIO.LOW)  # pull enable to low to enable motor
# motor 2 enable setup and ouput
GPIO.setup(EN_pin_m2, GPIO.OUT)  # set enable pin as output
GPIO.output(EN_pin_m2, GPIO.LOW)  # pull enable to low to enable motor


def motor1cal():  # calibration so linear motor knows where it is in relation to key cylinder
    global pulse, direction_m1, limit_m1
    direction_m1 = True
    while not limitswitch_m1_fwd.is_pressed:
        pulse = not pulse  
        motor1()
        sleep(.0002)


def motor1end():
    global travel_m1, pulse, direction_m1 
    travel_m1 = 7000
    direction_m1 = False
    for x in range(travel_m1): 
        pulse = not pulse  
        motor1()
        sleep(.0002)
    print("Done!", cyclesstart, " Cycles completed")


def motor1fwd():
    global pulse, direction_m1, cycles, limit_m1  
    direction_m1 = True
    while not limitswitch_m1_fwd.is_pressed:
        pulse = not pulse  
        motor1()
        sleep(.00008)
    else:
        cycles -= 1
        print("Cycles remaining: ", cycles)
        motor2turn()
        
def motor1rev():
    global pulse, direction_m1, cycles, limit_m1  
    direction_m1 = False
    while not limitswitch_m1_rev.is_pressed:
        pulse = not pulse  
        motor1()
        sleep(.0003)
#     else:
#         print("end 1 cycle")

def motor2turn():
    global pulse, direction_m2, cycles  
    for y in range(2):
        direction_m2 = not direction_m2  
        for x in range(travel_m2):  
            pulse = not pulse
            motor2()
            sleep(.001)
    else:
        motor1rev()
        
def motor1():
    GPIO.setup(step_pin_m1, GPIO.OUT)
    GPIO.setup(direction_pin_m1, GPIO.OUT)
    GPIO.output(step_pin_m1, pulse)  # toggle is the same a pulse/step
    GPIO.output(direction_pin_m1, direction_m1)  # LOW = CCW, HIGH = CW


def motor2():
    GPIO.setup(step_pin_m2, GPIO.OUT)
    GPIO.setup(direction_pin_m2, GPIO.OUT)
    GPIO.output(step_pin_m2, pulse)  # toggle is the same a pulse/step
    GPIO.output(direction_pin_m2, direction_m2)  # LOW = CCW, HIGH = CW


def main():
    motor1cal()

    input("Press Enter When Ready")
    while cycles > 0:
        motor1fwd()
    
    motor1end()

    GPIO.cleanup()  # clear GPIO allocations after run


# JDP: This wierd looking if statement is the entry point if you run the .py directly.  By doing it this way you can expose functions in the file for
#      use elsewhere or run it on its own.
if __name__ == '__main__':
    main()

