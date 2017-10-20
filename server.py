"""
Title: Group Chat using AWS Ec-2 as server
Author: Bharani Kodirangaiah

Run server program on AWS EC-2 and use the same port number in ur client code
"""

import socket
import sys
import select

mastersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mastersock.bind(('', 100))
mastersock.listen(5)

clientname = []
clientsock = []
#for sock in clientsock:
#	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
activeclients = 0
	
readlist = []
writelist = []
readlist.append(mastersock)

while 1:
	
	readready, writeready, eready = select.select(readlist, writelist, [])
	
	for socket in readready:
		if socket == mastersock:
			client, address = mastersock.accept()
			newclient = client
			readready.remove(mastersock)
			readlist.append(newclient)
			
		elif socket == newclient and socket not in clientsock:
			username = newclient.recv(50)
			clientname.append(username)
			clientsock.append(activeclients)
			clientsock[activeclients] = newclient
			print '%s has Joined chat' %(username)
			newclient.send(username)
			readready.remove(newclient)
			readlist.remove(newclient)
			readlist.append(clientsock[activeclients])
			activeclients += 1
			
		else:
			message = socket.recv(100)
			print message
			for sock in clientsock:
				if sock != socket:
					writelist.append(sock)
			readready.remove(socket)
			
	for socket in writeready:
		socket.send(message)
		writeready.remove(socket)
		writelist.remove(socket)

			
