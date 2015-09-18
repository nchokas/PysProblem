#UDP Server
from socket import *

#socket parameters
host = "localhost"
port = 5190
buf = 1024
addr = (host,port)

#create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

#receive messages
while 1:
    data,addr = UDPSock.recvfrom(buf)
    if not data:
        print "Client has exited!"
        break
    else:
        print "\nReceived message '", data,"'"

#close socket
UDPSock.close()
