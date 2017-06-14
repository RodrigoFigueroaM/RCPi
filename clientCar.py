#!/usr/bin/python env
import socket
import subprocess
import sys , codecs
from protocol import sendData, receiveData, sendFile
import os

def ephemeralSocket():
    ephemeral = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to firts available port
    ephemeral.bind(('',0))
    return ephemeral

def forward(sock):
    sendData(sock, 'w')
    serverData = receiveData(sock)
    print serverData

def reverse(sock):
    sendData(sock, 's')
    serverData = receiveData(sock)
    print serverData

def left(sock):
    sendData(sock, 'a')
    serverData = receiveData(sock)
    print serverData

def right(sock):
    sendData(sock, 'd')
    serverData = receiveData(sock)
    print serverData

def stop(sock):
    sendData(sock, 'l')
    serverData = receiveData(sock)
    print serverData

def cam(sock):
    sendData(sock, 'cam')
    serverData = receiveData(sock)
    try:
        # Create a TCP connection
        ephemeralPort = int(serverData)

        ephemeralSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        ephemeralSocket.connect((serverAddr, ephemeralPort))

        # Make socket from connection 
        camConnection = ephemeralSocket.makefile('rb')
        try:
            child = os.fork()
            if child == 0 :
                cmdline = ['vlc', '--demux', 'h264', '-']
                player = subprocess.Popen(cmdline, stdin = subprocess.PIPE )
                while True:
                    data = camConnection.read(1024)
                    if not data:
                        break
                    player.stdin.write(data)   
            os.exit(0) 
        finally:
            camConnection.close()
            player.terminate()
    finally:
        pass
# *****************************************************
# parses and handles meessages send from client
# @param socket -- socket where client connected
# *****************************************************
def printMenu():
    print('''

                ______  _____ ______ _ 
                | ___ \/  __ \| ___ (_)
                | |_/ /| /  \/| |_/ /_ 
                |    / | |    |  __/| |
                | |\ \ | \__/\| |   | |
                \_| \_| \____/\_|   |_|
                                       
                                       
        ---------------------------------------------------
                    Car Controller
                    W: Forward
                    A: Turn Left
                    S: Reverse
                    D: Turn Right

                    cam or camera : turn on camera
                    L: Stop
                    Quit: exit 
        ---------------------------------------------------
        ''')
        
        
def commandHandler(sock):
    printMenu()
    command = [inp for inp in raw_input('Car >').split()]
    cmd = command[-1].lower()
    while socket and cmd != 'quit':
        if cmd == 'w':
            forward(sock)
        elif cmd == 'a':
            reverse(sock)
        elif cmd == 's':
            left(sock)
        elif cmd == 'd':
            right(sock)
        elif cmd == 'l':
            stop(sock)
        elif cmd == 'cam' or cmd == 'camera':
            cam(sock)
        else:
            sendData(sock, cmd)
            serverData = receiveData(sock)
            print serverData
        command = [inp for inp in raw_input('Car >').split()]
        cmd = command[-1].lower()
        print 'COMMAND ', cmd
    sock.close()


#!/usr/bin/python env
# *****************************************************
# This file implements a ftp server 
# *****************************************************
import socket
import sys 

if __name__ == '__main__':
    if len( sys.argv ) != 3:
        print 'Usage: python ' , sys.argv[0] , ' <servermachine> <serverport> '
        exit(1)
    global serverAddr
    serverAddr = ''
    # Server address
    serverAddr = sys.argv[1]

    # Server port
    serverPort = int(sys.argv[2])

    # Create a TCP socket
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    connSock.connect((serverAddr, serverPort))

    # Keep connection
    try: 
        while True:
            commandHandler(connSock)
    except KeyboardInterrupt:
        connSock.close()
