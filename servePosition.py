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

firstScreenX = 590
secondScreenX = 620
thirdScreenX = 540

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
		print(xPos,yPos)
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
#		print("phi is %s" % phi)
#		yPos = 30*np.tan(np.pi*(60 + camHeight*(480 - float(theta))/240)/180) 			#probably less than 30 since this is the vertical
		fFd = 0.785398					#radians to degrees
		if phi < firstScreenX :
			yPos = 30*np.tan(np.pi*(60 + camHeight*(480 - float(theta))/240)/180)
			xPos = yPos*np.tan((phi-firstScreenX/2)*30/(firstScreenX/2))
			realX = xPos*np.cos(fFd) - yPos*np.sin(fFd)
			realY = xPos*np.sin(fFd) + yPos*np.cos(fFd)
			xPos = realX
			yPos = realY
		elif phi < (firstScreenX + secondScreenX): #center coordinate system
			yPos = 30*np.tan(np.pi*(60 + camHeight*(480 - float(theta))/240)/180)
			xPos = yPos*np.tan((phi-secondScreenX/2 - firstScreenX)*30/(secondScreenX/2))
		else:
			yPos = 30*np.tan(np.pi*(60 + camHeight*(480 - float(theta))/240)/180)
			xPos = yPos*np.tan((phi-thirdScreenX/2 - firstScreenX - secondScreenX)*30/(thirdScreenX/2))
			realX = xPos*np.cos(-fFd) - yPos*np.sin(-fFd)
			realY = xPos*np.sin(-fFd) + yPos*np.cos(-fFd)
			xPos = realX
			yPos = realY
    #  Send reply back to client
		

firstThread = threading.Thread(target=checkSocket)
firstThread.start()
secondThread = threading.Thread(target=thread_gui)
secondThread.start()


