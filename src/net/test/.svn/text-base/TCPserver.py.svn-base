#TCP Server
from socket import *
import sys
import pickle

#socket parameters
host = "localhost"  #must be IP address of machine
port = 12345
buf = 4096
addr = (host,port)

def create_socket():
    #create socket
    TCPSock = socket(AF_INET,SOCK_STREAM)
    #Make sure that we can still use the same addr even if it is in use already...
    TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #Bind address to socket
    TCPSock.bind(addr)
    print "TCPServer listening for Client on port", port ,"..."
    TCPSock.listen(1)  #listen for connection and only allow 1 simultaneous connection
    return TCPSock

def main():
    TCPSock = create_socket()
    object_dic = {}
    game_stat_dic = {}
    
    #receive testDic and display to the screen
    while 1:
        connection, address = TCPSock.accept() # connection is a new socket
        print "Client connected at", address[0]
        dic1 = connection.recv(4096) # receive the object_dic
        dic2 = connection.recv(4096) # receive the game_stat_dic
        if not dic1 and not dic1:
            print "Client has exited!"
            break
        else:
            print "\nReceived object_dic dictionary: ", pickle.loads(dic1)
            object_dic = pickle.loads(dic1)
            print "\nReceived game_stat dictionary: ", pickle.loads(dic2)
            game_stat_dic = pickle.loads(dic2)
            break
        
    print "Now that we have the object_dic dictionary we will print out the keys and values..."
    for x in object_dic:
        print "Key:", x, "  Value:", object_dic.get(x)
        
    print "Now that we have the game_stat_dic dictionary we will print out the keys and values..."
    for x in game_stat_dic:
        print "Key:", x, "  Value:", game_stat_dic.get(x)
    
    #close socket
    TCPSock.close()
    print "Server exited!"
    sys.exit()

if __name__ == '__main__':
    sys.exit(main())