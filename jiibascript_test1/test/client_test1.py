#!/usr/bin/env python3
import sys
sys.path.insert(0, '../proto')

import socket
import player_pb2
import tcp_packet_pb2

HOST = '202.92.144.45'  # The server's hostname or IP address
PORT = 80        # The port used by the server


player = player_pb2.Player()
player.name = "j" #input("Enter name: ")
player.id = '1'	#input("Enter person ID number: ")

msg = tcp_packet_pb2.TcpPacket()

msg.type = tcp_packet_pb2.TcpPacket.CONNECT
# connect_msg = msg.ConnectPacket.add() 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# print("connecting to the address", HOST, PORT);
    s.connect((HOST, PORT))
    s.sendall(bytes(msg))
    data = s.recv(1024)

print('Received', repr(data))