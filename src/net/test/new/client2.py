#test client 1
from socket import *
import sys
import pickle
import threading
import time
import random


print "client 2 --------"

class getData(threading.Thread):
    def __init__(self, soc):
        threading.Thread.__init__(self)
        self.TCPSock = soc
    def run(self):
        while True:
            data = self.TCPSock.recv(4096)
            if not data:
                continue
            else:
                print data
            if data == "done":
                break
        #for i in range(0,3):
            #print "get data thread: ",int(10*random.random())
            #time.sleep(int(10*random.random()))
            
#class sendData(threading.Thread):
#    def run(self):
#        for i in range(0,3):
#            print "send data thread ",int(10*random.random())
#            time.sleep(int(10*random.random()))
            
def sendData(soc, comp):
    for i in range(0,6):
        num = str(random.random())
        if i == 5:
            soc.send("done")
        else:
            if comp == "server":
                print "send to client:", num
                soc.send("receive from server: " + num)
            if comp == "client":
                print "send to server:", num
                soc.send("receive from client: " + num)
        time.sleep(int(10*random.random())+5)

def host():
    TCPSock = socket(AF_INET,SOCK_STREAM)
    TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    TCPSock.bind(('localhost', 12345))
    TCPSock.listen(2)
    while True:
        print "waiting for player to join..."
        connection, address = TCPSock.accept() # connection is a new socket
        print "Client connected at", address[0]
        get_data = getData(connection)
        get_data.start()
        sendData(connection, "server")
        #send_data = sendData()
        #send_data.start()
        #connection.send("Message From Server:  We can now play the game dude!!!")
        #connection.close()
        break
    time.sleep(10)
    TCPSock.close()

def join():
    ip = raw_input("Enter IP address of server: ")
    TCPSock = socket(AF_INET,SOCK_STREAM)
    TCPSock.connect((ip, 12345))
    get_data = getData(TCPSock)
    get_data.start()
    sendData(TCPSock, "client")
    #send_data = sendData()
    #send_data.start()
    #while True:
    #    data = TCPSock.recv(4096)
    #    if data: break
    #print data
    time.sleep(10)
    TCPSock.close()


option = raw_input("host(1) or join(2): ")
if option == '1':
    host()
if option == '2':
    join()
    
#time.sleep(20)
print "sent all data!!!!!  Now closing connection..."
sys.exit()