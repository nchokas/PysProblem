#test client 1
from socket import *
import sys
import pickle
from socket_struct import socObject

dictionary = {'one':1, 'two':2, 'three':3}
ip = 'localhost'

print "client 2 --------"

option = raw_input("host(1) or join(2): ")
if option == 1:
    host()
if option == 2:
    join()

def host():
    socket = socObject(ip)
    socket.create_server_socket()
    socket.connect_socket()
    socket.socket_listen()
    while True:
        print "waiting for player to join..."
        socket.connection, socket.address = socket.TCPSock.accept() # connection is a new socket
        if socket.address[0] != "":
            print "Client connected at", socket.address[0]
            socket.send_data("We can now play the game...")
            break

def join():
    ip = raw_input("Enter IP address of server: ")
    socket = socObject(ip)
    socket.create_client_socket()
    socket.connect_socket()
    socket.send_data("player joined game")
    data = socket.recv(4096)
    print pickle.loads(data)
    
#socket.send_data(dictionary)
socket.close_socket()
print "sent all data!!!!!  Now closing connection..."
sys.exit()