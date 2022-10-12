from tkinter import *
from time import sleep
import threading

window = Tk()
window.title("1500 Cycle Tester")
window.geometry('300x300')

combo1 = Label(window, text="Combo 1")
combo1.grid(column=0, row=0)

combo2 = Label(window, text="Combo 2")
combo2.grid(column=0, row=1)

combo3 = Label(window, text="Combo 3")
combo3.grid(column=0, row=2)

combo1txt = Entry(window,width=10)
combo1txt.grid(column=1, row=0)

combo2txt = Entry(window,width=10)
combo2txt.grid(column=1, row=1)

combo3txt = Entry(window,width=10)
combo3txt.grid(column=1, row=2)

cycles = Label(window, text="Number of Cycles")
cycles.grid(column=0, row=3)

cyclestxt = Entry(window,width=10)
cyclestxt.insert(0, "10")
cyclestxt.grid(column=1, row=3)

currentinfo = Label(window, text=" ")
currentinfo.grid(column=0, row=6)

global comboprint
comboprint = Label(window, text=" ")
comboprint.grid(column=0, row=7)

cyclesint = 1

def start():
    global cycles, cyclesint
    cyclesint= int(cyclestxt.get())
    res = "Cycles Remaining: " + str(cyclesint)
    currentinfo.configure(text= res)
    #cycles = cyclestxt.get
    thisismain()

def tothetop():
    thisismain()

#cyclesint= int(cyclestxt.get())

def passing():
    global incombo1, incomboall, blah, cyclesint
    incombo1 = combo1txt.get()
    incombo2 = combo2txt.get()
    incombo3 = combo3txt.get()
    incomboall = incombo1 + " / " + incombo2 + " / " + incombo3
    blah = "cycles remaining : " + str(cyclesint)
    comboprint.configure(text = blah)
    #print(blah)
    sleep(.1)

start = Button(window, text="Start", command=threading.Thread(target=start).start(), width=10)
start.grid(column=0, row=4)

stop = Button(window, text="Stop", command=start, width=10)
stop.grid(column=1, row=4)

relaysoff = Button(window, text="Relays Off", command=passing, width=10)
relaysoff.grid(column=0, row=5)
#window.mainloop()
def thisismain():
    global cycles, cyclesint, bike
    bike = cyclesint
    #window.mainloop()
    if cyclesint >= 1:
        while cyclesint >= 1:
            #print(blah)
            #print(bike)
            #bike -= 1
            blah = "cycles remaining : " + str(cyclesint)
            comboprint.configure(text = blah)
            #passing()
            print(cyclesint)
            cyclesint -= 1
            sleep(.5)
            #tothetop()
            print("bike was :", bike)
    else:
        print("something printed")        

window.mainloop()