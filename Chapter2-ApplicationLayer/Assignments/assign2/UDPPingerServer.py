#!/usr/bin/python
import random
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
portNumber = 12000
serverSocket.bind(('', portNumber))

while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(2048)
    message = message.upper()
    if rand < 4:
        continue
    serverSocket.sendto(message,address)

