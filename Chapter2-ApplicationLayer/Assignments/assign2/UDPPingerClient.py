#!/usr/bin/python

from socket import *
import time

def construct_message(idx):
    message = ('Ping', str(idx), str(time.time()))
    return ' '.join(message)

serverPort = 12000
serverName = '192.168.3.3'
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

nLost = 0
nTotal = 10

for i in range(0, nTotal):
    message = construct_message(i)
    clientSocket.sendto(message, (serverName, serverPort))

    try:
        modifiedMessage, serverAddr = clientSocket.recvfrom(2048)
        print 'Received return packet:', modifiedMessage
        curEpoch = time.time()
        sentEpoch = float(modifiedMessage.split(' ')[-1])
        print 'RTT =', str(curEpoch - sentEpoch), 's'
    except timeout:
        print 'Request timed out'
        nLost += 1

print 'Packet lost rate: ', str(nLost * 100.0 / nTotal), '%'
