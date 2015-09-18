 #test server
from socket import *
import sys
import pickle
from socket_struct import socObject
import threading
import time, random


dictionary = {}
socket = socObject()

print socket.host
print socket.addr
print socket.port
print socket.buffer

socket.create_server_socket()
socket.socket_listen()


class MyThread(threading.Thread):
    def run(self):
        for i in range(0,3):
            print "sleeping for ",int(10*random.random()), "seconds..."
            time.sleep(int(10*random.random()))
            #dictionary = socket.get_data()
               

#this while loop needs to be a thread...

for i in range(0,2):
    test = MyThread()
    test.start()

print "testttttttttt"
print "testttttttttt"
time.sleep(2)
print "testttttttttt"
print "testttttttttt"
time.sleep(2)
print "testttttttt"
print "socket closed..."

time.sleep(10)


   
sys.exit()
