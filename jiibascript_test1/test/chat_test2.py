#!/usr/bin/env python3
import sys 
sys.path.insert(0, '../proto')

import socket, threading 
import player_pb2
import tcp_packet_pb2


def opt():
	# packet = tcp_packet_pb2.TcpPacket()
	type = input("\n---------------------\n> O P T I O N S\n---------------------\n[1] - Connect \n[2] - Create a Lobby \n[3] - Chat \n[4] - Player List\n[0] - Disconnect  \nEnter option: ")
	return type

#Here the host will create a lobby. 
def Create_Lobby(packet):
	print("\n-------------------\n>> Create a Lobby\n")

	req = tcp_packet_pb2.TcpPacket.CreateLobbyPacket()
	req.type = packet.type
	req.max_players = int(input("Enter max number of players: "))


	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("creating a lobby...")
		s.connect((HOST, PORT))
		s.sendall(req.SerializeToString())
		data = s.recv(1024)

		upd = req
		upd.ParseFromString(data)
		try:
			print("> You may now connect to lobby: ", upd.lobby_id)
		except Exception as x:
			print(x.type, x.err_message)
		
		# Connect(upd)	

	return upd


#Here the player/host will connect to the lobby
def Connect(packet):
	print("\n-------------------\n>> Connect to Lobby\n")
	req = tcp_packet_pb2.TcpPacket.ConnectPacket()
	req.type = packet.type

	req.player.name = input("Enter player name: ")
	# req.player.id = "-1"
	req.lobby_id = input("Enter lobby id: ")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("connecting to", req.lobby_id, " ...")
		s.connect((HOST, PORT))
		s.sendall(req.SerializeToString())
		data = s.recv(1024)

		upd = req
		print(str(req))
		upd.ParseFromString(data)
		try:
			print("You may now start to chat in lobby: ", upd.lobby_id)
		except Exception as x:
			print(x.err_message)

		print(upd.type)

		# Chat(upd)
			
	return upd

#Here the player can send message to the other player in the lobby. 
#---Listening_thread()
def Chat(packet):
	print("\n-------------------\n>>\n")
	req = tcp_packet_pb2.TcpPacket.ChatPacket()
	req.type = packet.type

	req.message = input("Me: ")
	req.player.CopyFrom(packet.player)
	req.lobby_id = packet.lobby_id

	print(req.type,req.lobby_id, packet.lobby_id)
	while(True):
		if(req.message == "--opt"):
			return
		else:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((HOST, PORT))
				s.sendall(req.SerializeToString())
				data = s.recv(1024)

				upd = req
				upd.ParseFromString(data)
				try:
					print(upd.player.name,": ", upd.message)
				except Exception as x:
					print(x.err_message)
		
		req.message = input("Me: ")




#MAIN
HOST = '202.92.144.45'  # The server's hostname or IP address
PORT = 80        # The port used by the server

packet = tcp_packet_pb2.TcpPacket()

type = opt()
while(int(type) < 5):
	if type == "1":
		packet.type = tcp_packet_pb2.TcpPacket.CONNECT
		packet = Connect(packet)
	elif type == "2":
		packet.type = tcp_packet_pb2.TcpPacket.CREATE_LOBBY
		packet = Create_Lobby(packet)
	elif type == "3":
		packet.type = tcp_packet_pb2.TcpPacket.CHAT
		Chat(packet)
	elif type == "4":
		packet.type = tcp_packet_pb2.TcpPacket.PLAYER_LIST
		#Chat(packet)
	elif type == "0":
		packet.type = tcp_packet_pb2.TcpPacket.DISCONNECT
		#Chat(packet)
	else:
		print ("Unknown packet type")

	print("\n\n---maintenance---")
	print(str(packet))

	type = opt()





