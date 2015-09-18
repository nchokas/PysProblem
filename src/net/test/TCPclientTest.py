#TCP client
from socket import *
import sys
import pickle
import pymunk as pm

#socket parameters
host = "localhost"  #must be IP address of sever you wish to connect to
port = 12345
buf = 4096
addr = (host,port)

def main():
    #create test dictionary
    object_dic = {'one':1, 'two':2, 'three':3}
    game_stat_dic = {'four':4, 'five':5, 'six':6}
    
    print "Object Dictionary Before Pickle: ", object_dic
    print "Object Dictionary After Pickle: ", pickle.dumps(object_dic)
    print "Game Stat Dictionary Before Pickle: ", game_stat_dic
    print "Game Stat Dictionary After Pickle: ", pickle.dumps(game_stat_dic)
    
    TCPSock = create_socket()
    
    #send testDic and testSwing to server
    TCPSock.send(pickle.dumps(object_dic))
    print "Successfully sent Object Dictionary to server!"
    TCPSock.send(pickle.dumps(game_stat_dic))
    print "Successfully sent Game Stat Dictionary to server!"
    
    #close socket
    TCPSock.close()
    print "Client exited!"
    sys.exit()
    
#create socket
def create_socket():
    TCPSock = socket(AF_INET,SOCK_STREAM)
    #connect to host at specified port
    TCPSock.connect((host, port))
    return TCPSock

if __name__ == '__main__':
    sys.exit(main())