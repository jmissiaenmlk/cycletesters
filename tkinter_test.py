from time import sleep

# testing mode switching

def jogmode(x):
    for i in range(x):
        print("Jog mode")
        sleep(.5)
        break
def runmode(y):
    for i in range(y):
        print("run mode")
        sleep(.1)
        break


while True:
    modeselect = int((input("Enter mode 1 for jog, 2 for run ")))
    moves = int((input("Enter number of moves ")))

    if modeselect == 1:
        jogmode(moves)
    else:
        runmode(moves)
    check = input("do you want to move on? y for yes any key for no ")
    if check.upper() =="y": #go back to top
        jogmode(moves)
    print("Bye...")
    break #exit