#!/usr/bin/python env
# *****************************************************
# 
# *****************************************************
import socket
import picamera
import sys 
import time
from protocol import sendData, receiveData, sendFile
from car import Car

car = Car()
car.speed = 255

def ephemeralSocket():
    ephemeral = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to firts available port
    ephemeral.bind(('',0))
    return ephemeral

def forward(sock, command):
    sendData(sock, 'Success '+ command )
    car.moveForward()
    car.accelerate() 
    print 'car move forward'
   	
def reverse(sock, command):
    sendData(sock, 'Success '+ command )
    car.moveBackward()
    car.accelerate() 
    print 'car move reverse'

def left(sock, command):
    sendData(sock, 'Success '+ command )
    car.left()
    print 'car move left'

def right(sock, command):
    sendData(sock, 'Success '+ command )
    car.right()
    print 'car move right'

def stop(sock, command):
    sendData(sock, 'Success '+ command )
    car.stop()
    print 'car stop'

def cam(sock, command):
    #create ephemeral port
    ephemeral = ephemeralSocket()
    # send client the port number
    msg = str(ephemeral.getsockname()[1])
    sendData(sock, msg)
    ephemeral.listen(1)
    camConnection = ephemeral.accept()[0].makefile('wb')
    
    try:
    	camera = picamera.PiCamera()
    	camera.resolution = (1200, 1200)
    	camera.framerate = 25 

    	camera.start_preview()
    	time.sleep(2)
    	camera.start_recording(camConnection, format = 'h264')
    	camera.wait_recording(600)
    	camera.stop_recording()
    
    finally:
    	camConnection.close()

            
# *****************************************************
# parses and handles meessages send from client
# @param socket -- socket where client connected
# *****************************************************
def commandHandler(socket):
    command = receiveData(socket)
    command = command.split()
    command[0] = command[0].lower()
    print 'COMMAND ', command
    while socket and command[0] != 'quit':
        if command[0] == 'w':
            forward(socket, command[0])
        elif command[0] == 'a':
            reverse(socket, command[0])
        elif command[0] == 's':
            left(socket, command[0])
        elif command[0] == 'd':
            right(socket, command[0])
        elif command[0] == 'l':
            stop(socket, command[0])
        elif command[0] == 'cam':
            cam(socket, command[0])
        else:
            sendData(socket, 'FAIL \"' + command[0] + '\" not supported')
        command = receiveData(socket)
        command = command.split()
        command[0] = command[0].lower()
        print 'COMMAND ', command
    car.stop()
    socket.close()
    print 'SUCCESS', command


if __name__ == '__main__':
    if len( sys.argv ) != 2:
        print 'Usage: python', sys.argv[0] ,' <PORT NUMBER>'
        exit(1)
    # The port on which to listen
    listenPort = int(sys.argv[1])

    # Create a welcome socket. 
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    serverSock.bind(('', listenPort))

    # Start listening on the socket
    serverSock.listen(1)

    # Accept connections forever
    while True:
        try:
            print 'Waiting for connections on port ', listenPort
            # Accept connections
            clientSock, addr = serverSock.accept()

            print 'Accepted connection from client IP: %s port: %s ' %(addr[0], addr[1])
            # handle input from client
            commandHandler(clientSock)

        except (KeyboardInterrupt):
            print 'Interupt detected ctrl + c x_x'
            # Close our side
            if serverSock:
            	serverSock.close()
            break
