#UDP client
from socket import *
import pygame

#socket parameters
host = "24.250.11.8"
port = 21567
buf = 1024
addr = (host,port)

#create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)

print "\n", "===Enter message to send to server===";

#send messages
while 1:
    data = raw_input('>> ')
    if not data:
        break
    else:
        if(UDPSock.sendto(data,addr)):
            print "Sending message '",data,"'....."

#close socket
UDPSock.close()
