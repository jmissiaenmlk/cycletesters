from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
from rotary import Rotary
import utime as time

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                            # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
hpos = 6
rotary = Rotary(16,17,15) # dt, clk, sw
cycles = 0
cycles_start = cycles
led = Pin(25, Pin.OUT)
open_valve = Pin(0, Pin.OUT, value = 0)
close_valve = Pin(1, Pin.OUT, value = 0)
opened_switch = Pin(2, Pin.IN, Pin.PULL_DOWN)
closed_switch = Pin(3, Pin.IN, Pin.PULL_DOWN)
time_delay = .25

oled.fill(0)
oled.text("Door Cycler",hpos,4)
oled.text("Select Cycles",1,22)
oled.show()

def pull_door():
    if opened_switch.value() == True and closed_switch.value() == False:
        print("door was opened")
        sleep(time_delay)
    else:
        while opened_switch.value() == False:
            open_valve.on()
            print("open valve")
            sleep(time_delay)
            open_valve.off()
        
def push_door():
    if closed_switch.value() == True and opened_switch.value() == False:
        print("door was closed")
        sleep(time_delay)
    else:
        while closed_switch.value() == False:
            close_valve.on()
            print("push door")
            sleep(time_delay)
            close_valve.off()
            
        
def main():
    global cycles, cycles_start
    cycles_start = cycles
    while cycles > 0:
        pull_door()
        push_door()
        cycles -= 1
        oled.fill(0)

        # Add some text
        oled.text("Door Cycler",hpos,4)
        oled.text(str(cycles),45,22)
        oled.text("Cycles Remaining",1,38)
        # Finally update the oled display so the image & text is displayed
        oled.show()

        print("Number of cycles remaining: ", cycles)
        sleep(time_delay)
        
    oled.fill(0)
    oled.text("Done", hpos, 4)
    oled.text("Cycles Completed", 1, 22)
    oled.text(str(cycles_start),1, 38)
    oled.show()


def rotary_changed(change):
    global val, cycles
    if change == Rotary.ROT_CW:
        cycles = cycles + 10
        oled.fill(0)
        oled.text("Door Cycler",hpos,4)
        oled.text(str(cycles),45,22)
        oled.text("Press To Start",1,38)
        oled.show()
        #print("cycles ", cycles)
    elif change == Rotary.ROT_CCW:
        cycles = cycles - 1
        oled.fill(0)
        oled.text("Door Cycler",hpos,4)
        oled.text(str(cycles),45,22)
        oled.text("Press To Start",1,38)
        oled.show()
        #print("cycles ", cycles)
    elif change == Rotary.SW_PRESS:
        print('PRESS')
        oled.fill(0)
        oled.text("Door Cycler",hpos,4)
        oled.text(str(cycles),45,22)
        oled.text("Cycles Remaining",1,38)
        oled.show()
        main()
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')
        
rotary.add_handler(rotary_changed)

while True:
    time.sleep(0.1)
    
if __name__ == '__main__':
    main()



