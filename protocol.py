#!/usr/bin/python env
# ************************************************
# Creates a header for the data that will be send 
# by appending ten zeroes the file size 
#  sends given data over the given socket
# @param socket - the socket to send data 
# @param data - data that will be send over the socket
# @return dataSend - the bytes sent
# *************************************************
def sendData (socket, data):
	data = str(data)
	dataStrSize = str(len(data))
	while len(dataStrSize) < 10:
		dataStrSize = "0" + dataStrSize
	dataToSend = dataStrSize + data
	dataSend = 0
	dataSend = socket.send(dataToSend)
	return dataSend

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ''
	
	# The temporary buffer
	tmpBuff = ''
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff	

# ************************************************
# Creates a buffer to receive specified data number
# in case there is no data it returns 'quit' result 
# of not receiving data
# it coolaborates recvAll to parse data 
# @param socket - the socket to send data 
# @return data - the message/data received from other side
# *************************************************
def receiveData(socket):
	#initialize variables
	data = ""
	dataSize = 0
	dataBuffer = ""
	#check for size
	dataBuffer = recvAll(socket, 10)
	# check for a message
	if not dataBuffer:
		return 'quit'
	#cast to int
	dataSize = int(dataBuffer)
	#get rest of the command 
	data = recvAll(socket, dataSize)
	return data


# ************************************************
# Opens a file in read format, and gets the size
# sends  data over the given socket
# @param socket - the socket to send data 
# @param fileName - name of the file to send 
# @return numSent - the number of bytes  sent
# *************************************************
import os
def sendFile(socket , fileName):
	# The file data
	fileContent = None
	numSent = 0
	# Read the file 
	fileObj = open(fileName, "r")
	fileContent = fileObj.read(os.path.getsize(fileName))
	# Send the file
	while numSent < len(fileContent) :
		numSent += sendData(socket,fileContent[numSent:])
	fileObj.close()
	return numSent