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
cyclestxt.grid(column=1, row=3)

currentinfo = Label(window, text=" ")
currentinfo.grid(column=0, row=6)

global comboprint
comboprint = Label(window, text=" ")
comboprint.grid(column=0, row=7)

cyclesint = 0
cycles = cyclesint

def main():
    global cycles, cyclesint, bike
    bike = cyclesint
    while cyclesint > -1:
        blah = "Cycles Remaining : " + str(cyclesint)
        comboprint.configure(text = blah)
        res = "Cycles Requested: " + str(cycles)
        currentinfo.configure(text= res)
        cyclesint -= 1
        sleep(.25)
  

def start_program():
    global cycles, cyclesint
    cyclesint= int(cyclestxt.get())
    cycles = cyclesint
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
