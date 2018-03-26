#!/usr/bin/python

from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080
serverSocket.bind(('', serverPort))
serverSocket.listen(2)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

while True:
    print 'Ready to server...'
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    filename = message.split()[1]
    print 'filename is: '+  filename

    try:
        f = open(filename[1:], 'r')
        outputdata = f.read()
        print 'file founded!'
        connectionSocket.send('HTTP/1.1 200 OK')
        connectionSocket.send('Connection: close')

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
    except IOError:
        print 'An error happened'
        connectionSocket.send('HTTP/1.1 404 Not Found')
        connectionSocket.send('Connection: close')

    connectionSocket.close()
