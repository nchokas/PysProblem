#socket structure
from socket import *
import sys, traceback
import cPickle, zlib
import threading
import random
import time

#socket parameters
port = 12345
buffer = 4096

zlibBool = True

class acceptConn(threading.Thread):
    def __init__(self, soc):
        threading.Thread.__init__(self)
        self.soc = soc
        self.getDataThread = None
        self.sendDataThread = None
        self.fun = None
        self.running = True
    def run(self):
        pass
    def accept(self):
        #print self.fun
        print "waiting for player to join..."
        client_conn, address = self.soc.TCPSock.accept() # connection is a new socket    
        #if self.running == True:
        print "client connected at", address[0]    
        get_data = getData(client_conn, 'server')
        get_data.start()
        send_data = sendData(client_conn, 'server')
        send_data.start()
        self.getDataThread = get_data
        self.sendDataThread = send_data
        #print get_data
        #print send_data
        #print self.fun
        #self.fun()
        

class getData(threading.Thread):
    def __init__(self, soc, comp):
        threading.Thread.__init__(self)
        self.soc = soc
        self.comp = comp
        self.fun = None
    def run(self):
        try:
            if self.comp == "server":
                while True:
                    data = self.soc.recv(buffer)
                    #print "server data: ",data
                    if not data:
                        continue
                    else:
                        if self.fun:
                            try:
                                if zlibBool == True:
                                    dict = cPickle.loads(zlib.decompress(data))
                                if zlibBool == False:
                                    dict = cPickle.loads(data)
                                print "GET: ", dict
                            except EOFError:
                                break
                            else:
                                self.fun(dict)
                    if data == "done":
                        break
            if self.comp == "client":
                while True:
                    data = self.soc.TCPSock.recv(buffer)
                    #print "client data: ", data
                    if not data:
                        continue
                    else:
                        if self.fun:
                            try:
                                if zlibBool == True:
                                    dict = cPickle.loads(zlib.decompress(data))
                                if zlibBool == False:
                                    dict = cPickle.loads(data)
                                print "GET: ", dict
                            except EOFError:
                                break
                            else:
                                self.fun(dict)
                    if data == "done":
                        break
        except:
            print "error in getData thread..."
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            print "LINE=",traceback.tb_lineno(sys.exc_info()[2])
                
class sendData(threading.Thread):
    def __init__(self, soc, comp):
        threading.Thread.__init__(self)
        self.soc = soc
        self.comp = comp
    def run(self):
        pass
    def send(self, data):
        try:
            if self.comp == "server":
                
                if zlibBool == True:
                    dict = zlib.compress(cPickle.dumps(data),True)
                if zlibBool == False:
                    dict = cPickle.dumps(data)
                print "SEND "+str(len(dict))+":", data
                self.soc.send(dict)
            if self.comp == "client":
                if zlibBool == True:
                    dict = zlib.compress(cPickle.dumps(data),True)
                if zlibBool == False:
                    dict = cPickle.dumps(data)
                print "SEND "+str(len(dict))+":", data
                self.soc.TCPSock.send(dict)
        except:
            print "error in sendData thread..."
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            print "LINE=",traceback.tb_lineno(sys.exc_info()[2])

    def testy(self):
        print "sendData Thread testyyyyy"
                       
class socObject(object):
    def __init__(self, host):
        self.host = host  
        self.port = port
        self.buffer = buffer
        self.addr = (self.host,self.port)
        self.TCPSock = None
    
    def create_server_socket(self):
        try:
            self.TCPSock = socket(AF_INET,SOCK_STREAM)
            self.TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.TCPSock.setsockopt(SOL_SOCKET, SO_RCVBUF, buffer)
            print "Initial socket buffer size:", self.TCPSock.getsockopt(SOL_SOCKET, SO_RCVBUF)
            self.TCPSock.bind(self.addr)
            self.TCPSock.listen(2)
        except error, (value,message): 
            if self.TCPSock:
                self.TCPSock.close()
            print "Unable to open socket: ", message
        
    def create_client_socket(self):
        try:
            self.TCPSock = socket(AF_INET,SOCK_STREAM)
            self.TCPSock.connect(self.addr)   
        except error, (value,message):
            if self.TCPSock:
                self.TCPSock.close()
            print "Unable to open socket: ", message  
  