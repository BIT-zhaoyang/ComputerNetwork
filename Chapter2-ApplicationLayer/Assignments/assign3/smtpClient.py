#!/usr/bin/python

import socket,ssl,base64

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
mailServer = ("smtp.163.com", 465)

# Build safe  connect
context = ssl.create_default_context()
sslSocket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname="smtp.163.com")
sslSocket.connect(mailServer)
recv = sslSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

# Send HELO command and print server response
heloCommand = 'HELO ZhaoYang \r\n'
sslSocket.send(heloCommand)
recv = sslSocket.recv(1024)
print recv
if recv[:3] != '250':
    print '250 reply not received from server.'

# Safe login
user = "japan07033407702@163.com"
passwd = "LXkU54SC7gNQWJoV"

authCommand = 'AUTH LOGIN\r\n'
sslSocket.send(authCommand)
recv = sslSocket.recv(1024)
print recv
if recv[:3] != '334':
    print '334 reply not received from server.'

sslSocket.send(base64.b64encode(user) + '\r\n')
recv = sslSocket.recv(1024)
print recv
if recv[:3] != '334':
    print '334 reply not received from server.'

sslSocket.send(base64.b64encode(passwd) + '\r\n')
recv = sslSocket.recv(1024)
print recv
if recv[:3] != '235':
    print '235 reply not received from server. Login failed.'

# Send MAIL FROM command and print server response.
mailfromCommand = 'MAIL FROM: <japan07033407702@163.com>\r\n'
sslSocket.send(mailfromCommand)
print sslSocket.recv(1024)

# Send RCPT TO command and print server response
rcpttoCommand = 'RCPT TO: <japan07033407702@163.com>\r\n'
sslSocket.send(rcpttoCommand)
print sslSocket.recv(1024)

# Send DATA command and print server response
sslSocket.send('DATA\r\n')
print sslSocket.recv(1024)

# Send message data.
message = """Subject: How to send an email using SMTP

Hello World! I love you! 
This is not a spam email, but a test one. Don\'t intercept this please!
The record needs to be set straight once and for all.

I'm absolutely trying to give you something and asking for nothing in return so you can just cash me outside how bow dah?

In all seriousness. This E-Book I'm giving you won't c0st you a dime or penny. But, it won't be around forever. After 7 days, I'm snatching it away. (I don't believe in no takey backeys).

If you wanna check it out just hit that link below and you'll be blessed with all types of knowledge.

Cash Me Outside

Peace,

Austin Dunham

PS: If she actually had the chance to read this E-Book she probably wouldn't have ever lost that fight in the first place. (Just Saying)

PPS: What are you doing at the bottom of this email? The clock is taking. Take advantage of this sweet deal before it goes away forever.
\r\n.\r\n"""
sslSocket.send(message)
print sslSocket.recv(1024)

# QUIT
sslSocket.send('QUIT\r\n')
print sslSocket.recv(1024)

