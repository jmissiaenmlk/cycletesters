#!/usr/bin/python -i

from tkinter import *
from time import sleep
import threading

window = Tk()
window.title("1500 Cycle Tester")
window.geometry('300x300')

cyclesint = 0
#cyclesint = IntVar()
cycles = cyclesint
combo1 = IntVar()
combo2 = IntVar()
combo3 = IntVar()

combo1label = Label(window, text="Combo 1")
combo1label.grid(column=0, row=0)

combo2label = Label(window, text="Combo 2")
combo2label.grid(column=0, row=1)

combo3label = Label(window, text="Combo 3")
combo3label.grid(column=0, row=2)

combo1txt = Entry(window,width=10)
combo1txt.grid(column=1, row=0)

combo2txt = Entry(window,width=10)
combo2txt.grid(column=1, row=1)

combo3txt = Entry(window,width=10)
combo3txt.grid(column=1, row=2)

cycleslabel = Label(window, text="Number of Cycles")
cycleslabel.grid(column=0, row=3)

cyclestxt = Entry(window,width=10)
#cyclestxt = Entry(window,width=10, textvariable = cyclesint)
cyclestxt.grid(column=1, row=3)

currentinfo = Label(window, text=" ")
currentinfo.grid(column=0, row=6)

cyclesremaininglable = Label(window, text=" ")
cyclesremaininglable.grid(column=0, row=7)

report1lable = Label(window, text=" ")
report1lable.grid(column=0, row=8)

#cyclesint = IntVar()
#cyclesint = 0
#cycles = cyclesint

def main():
    global cycles, cyclesint
    while cyclesint > -1:
        cyclehelper = "Cycles Remaining : " + str(cyclesint)
        cyclesremaininglable.configure(text = cyclehelper)
        requestedhelper = "Cycles Requested: " + str(cycles)
        currentinfo.configure(text= requestedhelper)
        combohelper = "selected combo: " + str(combo1)+ "/"+ str(combo2) +"/" +str(combo3)
        report1lable.configure(text = combohelper)
        cyclesint -= 1
        sleep(.25)
  

def start_program():
    global cycles, cyclesint, combo1, combo2, combo3
    cyclesint= int(cyclestxt.get())
    cycles = cyclesint
    combo1 = int(combo1txt.get())
    combo2 = int(combo2txt.get())
    combo3 = int(combo3txt.get())
    main()

def relay_reset():
    print("turn off relays")

def stop_program():
    print("Stop Program")
    global cyclesint
    cyclesint= 0
    main()


startbutton = Button(window, text="Start", command=threading.Thread(target=start_program).start, width=10)
startbutton.grid(column=0, row=4)

stop = Button(window, text="Stop", command=start_program, width=10)
stop.grid(column=1, row=4)

relaysoff = Button(window, text="Relays Off", command=relay_reset, width=10)
relaysoff.grid(column=0, row=5)

window.mainloop()
