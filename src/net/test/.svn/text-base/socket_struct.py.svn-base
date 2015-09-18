#socket structure
from socket import *
import sys
import pickle
from threading import *

#socket parameters
ip = '121.215.27.103'  #ip of current machine
port = 12345
buffer = 4096

class socObject(object):
    
    def __init__(self, host=ip):
        self.host = host  
        self.port = port
        self.buffer = buffer
        self.addr = (self.host,self.port)
    
    def create_server_socket(self):
        self.TCPSock = socket(AF_INET,SOCK_STREAM)
        self.TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.TCPSock.bind(self.addr)
        
    def create_client_socket(self):
        self.TCPSock = socket(AF_INET,SOCK_STREAM)
        
    def connect_socket(self):
        self.TCPSock.connect((self.host, self.port))

    def close_socket(self):
        self.TCPSock.close()
        
    def send_data(self, dictionary):
        self.TCPSock.send(pickle.dumps(dictionary))
        
    def socket_listen(self):
        self.TCPSock.listen(1)  #listen for connection and only allow 1 simultaneous connection
            
    def get_data(self): 
        while 1:
            print "waiting for connection"
            self.connection, self.address = self.TCPSock.accept() # connection is a new socket
            print "Client connected at", self.address[0]
            #thread.start_new_thread(handler, (self.connection, self.address)
            data = self.connection.recv(4096) # receive the dictionary
            if not data:
                print "Client has exited!"
                break
            else:
                dic = pickle.loads(data)
                print "\nReceived dictionary: ", dic
                print "Now that we have the object_dic dictionary we will print out the keys and values..."
                for x in dic:
                    print "Key:", x, "  Value:", dic.get(x)
                #return dic
    
    