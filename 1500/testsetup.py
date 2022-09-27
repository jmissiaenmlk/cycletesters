import time

currentPosition = 0
combo1 =int(input("enter combo 1 "))
combo2 =int(input("enter combo 2 "))
combo3 =int(input("enter combo 3 "))
stepCount = 0
codeCount = 0
direction = 1 #1 = CW 0 = CCW
cycle = int(input("enter Cycle Count "))
pulse = 0

def motorspin1(turn1):
    global currentPosition, cycle, direction, pulse
    direction = 1
    for p in range(10):
        pulse = not pulse
        time.sleep(.1)
        for p in range(40 - combo1):
            pulse = not pulse
            time.sleep(.1)
        currentPosition == combo1

def motorspin2(turn1):
    global currentPosition, cycle, direction, pulse
    direction = 0
    for p in range(10):
        pulse = not pulse
        time.sleep(.1)
        if combo2 > combo1:
            for p in range(combo2 - combo1):
                pulse = not pulse
                time.sleep(.1)
                currentPosition += 1
        elif combo2 < combo1:
            for p in range((40 - combo1)+ combo2):
                pulse = not pulse
                time.sleep(.1)
                currentPosition += 1
            currentPosition == currentPosition -40

def motorspin3(turn1):
    global currentPosition, cycle, direction, pulse
    direction = 1
    if combo3 > combo2:
        for p in range((combo2 + 40)- combo3):
            pulse = not pulse
            time.sleep(.1)
            currentPosition -= 1
        currentPosition == currentPosition + 40   
    elif combo3 < combo2:
        for p in range(combo2- combo3):
            pulse = not pulse
            time.sleep(.1)
            currentPosition -= 1

while cycle >= 0:
    motorspin1(combo1)
    print(currentPosition)
    motorspin2(combo2)
    print(currentPosition)
    motorspin3(combo3)
    print(currentPosition)
    cycle -= 1
else:
    print("done")

#Pos1 = move cw 40 then 40 - combo1
#Pos2 = move ccw 40 then ((40 - combo1)+combo2) 
# if combo 2 is > combo1 then combo2 - combo1
# if combo 2 is < combo1 then ((40 -combo1)+combo2)
#Pos3 = move cw combo2 - combo3
# if combo3 > combo2 then combo2 + 40 - combo3
# if combo3 < combo2 then combo2 - combo3
#currentPos = Pos1
#26 direction 19 step