"""
Title: Group Chat using AWS Ec-2 as server
Author: Bharani Kodirangaiah

Group Chat using Amazon AWS EC-2 server, Clientgui.py is client code, multiple user can share this client code. Running client on each machine makes them to connect with each other
Following program opens a group chat GUI, through which connected user can exchange text file or file with each other.
"""


import socket
import select
import sys
from Tkinter import *
import thread
import gui 
from tkFileDialog import *
import os
import time

username = ''
serverdata = ''
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address=''   #key in ip address 
serversock.connect((ip_address, 100)) #replace 100 with ur choice of ur port number

username = raw_input('Enter username\n')
serversock.send(username)
buf = serversock.recv(50)
if buf == username:
	print 'Successfully added into chat\n'
else:
	print 'Client not added in chat, exiting program\n'
	sys.exit()

def selectloop(serversock):
	global serverdata, messagewindow
	print 'Enter selectloop\n'
	readlist = []
	writelist = []
	readlist.append(serversock)
	readlist.append(sys.stdin)

	while 1:
		readready, writeready, eready = select.select(readlist, writelist, [])
	
		for socket in readready:
			if socket == serversock:
				serverdata = serversock.recv(100)
				if "file is shared" in serverdata:
					name_user=serverdata.split(":")[1]					
					file_1=os.path.basename(serverdata.split(":")[-1])
					pop_up(serverdata,name_user, file_1)
					
					print "name of user sent %s"%name_user
				else:
					serverdata = serverdata + '\n'
					messagewindow.insert(END, serverdata)
				print (serverdata)
		
			elif socket == sys.stdin:
				data = sys.stdin.readline()
				length= len(data)
				inputmessage = username + ':' + data[0:length - 1]
				writelist.append(serversock)
			
		for socket in writeready:
			if socket == serversock:
				serversock.send(inputmessage)
				writelist.remove(serversock)
				writeready.remove(serversock)
				
				
thread.start_new_thread(selectloop, (serversock,))


"""
Creating GUI using tkinter in python
"""
	
chatwindow = Tk()

chatwindow.wm_title("Chat Box: %s" %username)
chatwindow.resizable('1','1')


def send_handler():
	message = entrybox.get()
	#lenght = len(message)
	message = username + ':' + message + '\n'
	messagewindow.insert(END, message)
	messagewindow.see(END)
	entrybox.delete(0, END)
	serversock.send(message[0:-1])

def send_file():
        filename = askopenfilename()
	print filename
	name=os.path.basename(filename)
	print "filename sent is %s" %name	
	#key_path = /home/bharanikodi/Projects/socketprog/DistributedProject.pem
        if(len(filename) > 0 and os.path.isfile(filename)):  
	    print "UI: Selected file: %s" % filename
	    os.system("scp -i /home/bharanikodi/Projects/socketprog/DistributedProject.pem %s ec2-user@54.149.180.219:/home/ec2-user/client_files"%filename)
	    
	    message= "file is shared:%s:/home/ec2-user/client_files/%s" %(username,name)
	    serversock.send(message)        
	else:
            print "UI: File operation canceled"

def pop_up(data,name_user,file_1):
	messagewindow.insert(END,"%s shared file %s"%(name_user,file_1))        
	popup = Tk()
    	popup.wm_title("Download file")
	popup.resizable('1','1')
	NORM_FONT= ("Verdana", 10)
    	label = Label(popup, text="Click DOWNLOAD to download the shared file", font=NORM_FONT)
    	label.pack(side="top", fill="x", pady=10)
	name=data.split(':')[-1]
	cwd = os.getcwd()
	print "gloabal inside popup %s" %name
	transfer = "scp -i /home/bharanikodi/Projects/socketprog/DistributedProject.pem ec2-user@54.149.180.219:%s %s" %(name,cwd)
	print("before button")
	time.sleep(5)
    	B1 = Button(popup, text="Download", command = lambda: os.system(transfer) or popup.destroy())
    	B1.pack(side=LEFT)
	B1 = Button(popup, text="Cancel", command = popup.destroy)
    	B1.pack(side=RIGHT)
    	popup.mainloop()

send = Button(chatwindow, text='Send', command=send_handler, activebackground = 'green')
file1 = Button(chatwindow, text='file', command=send_file, activebackground = 'green')
scrollbar = Scrollbar(chatwindow)
scrollbar.pack(side=RIGHT, fill=Y)
messagewindow = Text(chatwindow, yscrollcommand=scrollbar.set, width=50, height=30)
scrollbar.config(command = messagewindow.yview)
message = StringVar()
entrybox = Entry(chatwindow, textvariable = message)
messagewindow.pack(side=TOP, fill=BOTH)
entrybox.pack(side=TOP, fill=BOTH)
send.pack(side=LEFT)
file1.pack(side=RIGHT)
chatwindow.bind('<Return>',send_handler)
chatwindow.mainloop()

	
