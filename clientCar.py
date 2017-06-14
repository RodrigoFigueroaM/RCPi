import socket
import subprocess
import sys, codecs
#!/usr/bin/python env
import socket
import sys 
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


# camera prtty much send shit and receive camera info in other port and ppen shit to se data
# def camera(socket):
#     #create ephemeral port
#     ephemeral = ephemeralSocket()
#     # send client the port number
#     msg = str(ephemeral.getsockname()[1])
#     sendData(socket, msg)
#     ephemeral.listen(1)
#     while True:
#         #once connected start sending file
#         sock, addr = ephemeral.accept()
#         if sock:
#             fileData = receiveData(sock)
#             fileContent = open('./server/' + fileName, "w")
#             fileContent.write(fileData)
#         sock.close()
#         print 'FILE: %s added to collection' %(fileName)
#         break

        
# *****************************************************
# parses and handles meessages send from client
# @param socket -- socket where client connected
# *****************************************************
def commandHandler(sock):
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

                    L: Stop
                    Quit: exit 
        ---------------------------------------------------
        ''')
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

# if __name__ == '__main__':
#     if len( sys.argv) != 2:
#         print 'Usage: python', sys.argv[0] ,' <PORT NUMBER>'
#         exit(1)

#     # The port on which to listen
#     listenPort = int(sys.argv[1])

#     # Create a welcome socket. 
#     serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Bind the socket to the port
#     serverSock.bind(('', listenPort))

#     # Start listening on the socket
#     serverSock.listen(1)

#     # Accept a single connection and make a file-like object out of it
#     connection = serverSock.accept()[0].makefile('rb')
#     try:
#         # Run a viewer with an appropriate command line. Uncomment the mplayer
#         # version if you would prefer to use mplayer instead of VLC
#         cmdline = ['vlc', '--demux', 'h264', '-']
#         player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
#         while True:
#             # Repeatedly read 1k of data from the connection and write it to
#             # the media player's stdin2

#             try:
#                 print 'Waiting for connections on port ', listenPort
#                 # Accept connections
#                 clientSock, addr = serverSock.accept()

#                 print 'Accepted connection from client IP: %s port: %s ' %(addr[0], addr[1])
#                 # handle input from cleint
#                 commandHandler(clientSock)

#             except (KeyboardInterrupt):
#                 print 'Interupt detected ctrl + c x_x'
#                 # Close our side
#                 if serverSock:
#                     serverSock.close()
#                 break
#                 player.stdin.write(data)

#     finally:
#         connection.close()
#         serverSock.close()
#         player.terminate()
