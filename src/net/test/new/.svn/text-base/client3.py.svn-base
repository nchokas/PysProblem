#test client 1
from socket import *
import sys
import time
import cPickle
from socket_struct import socObject


print "client 3 --------"
server_ip = "127.0.0.1"
object_dict = {'name':'object', 'stage':'stage', 'pos_x':23, 'pos_y':45,'circle_mass':12, 'radius':10, 'circle_elasticity':1, 'color':'purple'}
stat_dict = {'name':'stat','points':244, 'balls_destroyed':5, 'balls_on_screen':15}

def host():
    soc = socObject(server_ip)
    soc.create_server_socket()
    print "waiting for player to join..."
    client_conn, address = soc.TCPSock.accept() # connection is a new socket
    print "Client connected at", address[0]
    soc.get_data(client_conn, "server")
    soc.send_data(client_conn, "server", object_dict)
    time.sleep(30)
    soc.TCPSock.close()

def join():
    ip = raw_input("Enter IP address of server: ")
    soc = socObject(ip)
    soc.create_client_socket()
    soc.get_data(soc, "client")
    soc.send_data(soc, "client", stat_dict)
    time.sleep(30)
    soc.TCPSock.close()


option = raw_input("host(1) or join(2): ")
if option == '1':
    host()
if option == '2':
    join()
    
#time.sleep(20)
print "sent all data!!!!!  Now closing connection..."
sys.exit()