#test client
from socket import *
import sys
import pickle
from socket_struct import socObject

dictionary = {'one':1, 'two':2, 'three':3}
ip = '24.250.11.8'
socket = socObject(ip)

print socket.host
print socket.addr
print socket.port
print socket.buffer

socket.create_client_socket()
socket.connect_socket()
socket.send_data(dictionary)
socket.close_socket()
print "sent dictionary!!!!!  Now closing connection..."
sys.exit()