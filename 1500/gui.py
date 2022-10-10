from tkinter import *

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

def clicked():
    res = "Cycles remaining: " + cyclestxt.get()
    currentinfo.configure(text= res)

start = Button(window, text="Start", command=clicked, width=10)
start.grid(column=0, row=4)

stop = Button(window, text="Stop", command=clicked, width=10)
stop.grid(column=1, row=4)

relaysoff = Button(window, text="Relays Off", command=clicked, width=10)
relaysoff.grid(column=0, row=5)

window.mainloop()