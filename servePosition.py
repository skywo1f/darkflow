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
global xPos
xPos = 0
camHeight = 52
def thread_gui():
	window = Tk()
	window.title("Distance approximator")
	window.geometry('1200x400')
	lbl = Label(window,text="Distance is (in) :")
	lbl.grid(column=0,row=0)
	lbl.config(font=("Courier", 44))
	while True:		
		labelVar = Label(window, text=int(yPos))
		labelVar.config(font=("Courier", 100))
		labelVar.grid(column=1,row=0)
		labelVar2 = Label(window, text=int(xPos))
		labelVar2.config(font=("Courier",100))
		labelVar2.grid(column=1,row=1)
		window.update()
#		print(yPos)
	window.mainloop()

def checkSocket():
	while True:
		global yPos
		global xPos
    #  Wait for next request from client
		message = socket.recv()
		socket.send(b"confirmed")
		alphabet = message.decode('utf-8')
		data = re.split(' ',alphabet)
		theta = float(data[0])
		phi = float(data[1])
		print("phi is %s" % phi)
		yPos = 30*np.tan(np.pi*(60 + camHeight*(480 - float(theta))/240)/180) 			#probably less than 30 since this is the vertical
		xPos = yPos*np.tan((phi-320)*30/320)
    #  Do some 'work'
#    time.sleep(1)

    #  Send reply back to client
		

firstThread = threading.Thread(target=checkSocket)
firstThread.start()
secondThread = threading.Thread(target=thread_gui)
secondThread.start()


