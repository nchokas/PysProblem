#test client 1
from socket import *
import sys
import time
import cPickle, threading
from socket_struct import *


print "client--------"
server_ip = "127.0.0.1"
object_dict = {'name':'circle', 'pos_x':23, 'pos_y':45,'radius':10, 'color':'purple'}
object_dict2 = {'name':'polygon', 'pos_x1':23, 'pos_y1':45,'pos_x2':23, 'pos_y2':45, 'radius':10, 'color':'purple'}
stat_dict = {'name':'stat','points':244}

def host():
    soc = socObject(server_ip)
    soc.create_server_socket()
    print "waiting for player to join..."
    client_conn, address = soc.TCPSock.accept() # connection is a new socket
    print "Client connected at", address[0]
    get_data = getData(client_conn, 'server')
    get_data.start()
    send_data = sendData(client_conn, 'server')
    send_data.start()
    print "test", get_data.comp
    while True:
        data = raw_input('--> ')
        if data == 'done':
            send_data.send('done')
            soc.TCPSock.close()
            break
        else:
            send_data.send(object_dict)
        

def join():
    ip = raw_input("Enter IP address of server: ")
    soc = socObject(ip)
    soc.create_client_socket()
    get_data = getData(soc, 'client')
    get_data.start()
    send_data = sendData(soc, 'client')
    send_data.start()
    print "test", get_data.comp
    while True:
        data = raw_input('--> ')
        if data == 'done':
            send_data.send('done')
            soc.TCPSock.close()
            break
        else:
            send_data.send(stat_dict)


option = raw_input("host(1) or join(2): ")
if option == '1':
    host()
if option == '2':
    join()
    
#time.sleep(20)
print "sent all data!!!!!  Now closing connection..."
sys.exit()