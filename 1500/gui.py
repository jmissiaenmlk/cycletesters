from tkinter import *
from time import sleep
import threading

window = Tk()
window.title("1500 Cycle Tester")
window.geometry('300x300')

cyclesint = IntVar()
cycles = cyclesint

def basicprogram():
    global cycles, cyclesint
    while cyclesint > -1:
        #cyclehelper = "Cycles Remaining : " + str(cyclesint)
        #comboprint.configure(text = cyclehelper)
        requestedhelper = "Cycles Requested: " + str(cyclesint)
        currentinfo.configure(text= requestedhelper)
        cyclesint -= 1
        sleep(.25) 
        startthis()

def startthis():
    global cycles, cyclesint
    cyclesint= int(currentinfo.get())
    cycles = cyclesint
    #main()
    
#def main():
#global currentinfo, cyclesint
cycleslabel = Label(window, text="Number of Cycles")
cycleslabel.grid(column=0, row=3)

cyclestxt = Entry(window,width=10, textvariable = cyclesint)
#cyclestxt = Entry(window,width=10, text="10")
cyclestxt.grid(column=1, row=3)

if cyclestxt.get() != "":
    #cyclesint = int(cyclestxt.get())
    cyclestxt.get()


currentinfo = Label(window, text=" ")
currentinfo.grid(column=0, row=6)

startb = Button(window, text="Start", command=threading.Thread(target=basicprogram).start, width=10)
startb.grid(column=0, row=4)

res = "Cycles Remaining: " , cyclesint
currentinfo.configure(text= res)

    #window.mainloop()



window.mainloop()      
# if __name__ == '__main__':
#     main()