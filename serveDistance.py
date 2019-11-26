from tkinter import *
import time
import zmq
import threading
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
global yPos
yPos = 0
camHeight = 55
def thread_gui():
	window = Tk()
	window.title("Distance approximator")
	window.geometry('1200x100')
	lbl = Label(window,text="Distance is :")
	lbl.grid(column=0,row=0)
	lbl.config(font=("Courier", 44))
	while True:		
		labelVar = Label(window, text=yPos)
		labelVar.config(font=("Courier", 44))
		labelVar.grid(column=1,row=0)
		window.update()
		print(yPos)
	window.mainloop()

def checkSocket():
	while True:
		global yPos
    #  Wait for next request from client
		message = socket.recv()
	
		output = message.decode('utf-8')
		print("position is %s" % output)
		yPos = 30*np.tan(np.pi*(60 + camHeight*(480 - float(output))/240)/180)
    #  Do some 'work'
#    time.sleep(1)

    #  Send reply back to client
		socket.send(b"confirmed")

firstThread = threading.Thread(target=checkSocket)
firstThread.start()
secondThread = threading.Thread(target=thread_gui)
secondThread.start()


