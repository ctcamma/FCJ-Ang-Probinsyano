#!/usr/bin/env python3
import sys 
sys.path.insert(0, '../proto')

import socket, threading 
import player_pb2
import tcp_packet_pb2
from threading import Thread
import time


#prints all the possible options in the chat.
def opt():
	print("\n------------------------------")
	print  ("|> C O M M A N D S           |")
	print  ("------------------------------")	
	print  ("| [ 1 ] - connect to a lobby |")
	print  ("| [ 2 ] - create a lobby     |")
	print  ("| [ 3 ] - go to chat         |")
	print  ("| [ 4 ] - player list        |")
	print  ("| [ 0 ] - disconnect         |")
	# print  ("| [ 5 ] - exit               |")
	print  ("---------------------------------")	
	type =  input("|>")
	return type

#Host creates a lobby. 
def Create_Lobby(s):
	print("\n-------------------\n>> Create a Lobby\n")

	#initialization of the Create Lobby Packet
	req = tcp_packet_pb2.TcpPacket.CreateLobbyPacket()
	req.type = 2
	req.max_players = int(input("Max number of players: "))

	print("|> creating a lobby...")
	s.sendall(req.SerializeToString())
	time.sleep(2)

	# data = s.recv(1024)

	# p = tcp_packet_pb2.TcpPacket()
	# p.ParseFromString(data)

	# if(p.type != 2):
	# 	p = p.ErrPacket()
	# 	p.ParseFromString(data)
	# 	print("* Error Code", p.type, "-",p.err_message)
	# else:
	# 	p = p.CreateLobbyPacket()
	# 	p.ParseFromString(data)
	# 	print("> Lobby created. You may now connect to lobby: ", p.lobby_id)

#Player/host connects to the lobby
#wala kang nakukuhang reply from the SERVER
def Connect(s):
	print("\n-------------------\n>> Connect to Lobby\n")
	
	# initialization of the request connect packet
	req = tcp_packet_pb2.TcpPacket.ConnectPacket()
	req.type = 1

	req.player.name = input("Player name: ")
	req.player.id = "-1"
	req.lobby_id = input("Lobby id: ")

	s.sendall(req.SerializeToString())
	print ("|> connecting ...")
	# time.sleep(2)
	

#Player enable to send message to the server then the server will broadcast it to all player in the lobby.
def Chat(s, p):
	print("\n-------------------\n|>Enter \"--opt\" to show chat options.\n")
	
	# Initialization of the request chat packet
	req = tcp_packet_pb2.TcpPacket.ChatPacket()
	req.type = 3

	try:
		req.player.CopyFrom(p.player)
		req.lobby_id = p.lobby_id 
	except Exception as x:
		print("")
	req.message = input()

	while(True):
		if(req.message == "--opt"):
			return 1
		else:
			s.sendall(req.SerializeToString())
			
		req.message = input()

def PlayerList(s):
	print("\n-------------------\n> Showing all players in the Lobby.\n")

	req = tcp_packet_pb2.TcpPacket.PlayerListPacket()
	req.type = 4

	s.sendall(req.SerializeToString())
	time.sleep(2)


def Disconnect(s, p):
	print("\n-------------------\n")

	req = tcp_packet_pb2.TcpPacket.ChatPacket()
	req.type = 3
	req.message = "--disconnecting"
	try:
		req.player.CopyFrom(p.player)
	except Exception as x:
		print(" ")
	s.sendall(req.SerializeToString())

	req = tcp_packet_pb2.TcpPacket.DisconnectPacket()
	req.type = 0

	try:
		req.player.CopyFrom(p.player)
	except Exception as x:
		print(" ")

	s.sendall(req.SerializeToString())


class listenThread(Thread): 
	def __init__(self, socket): 
		Thread.__init__(self) 
		self.s = socket

		self.running = True

		self.open = False
        # print "[+] New server socket thread started for " + ip + ":" + str(port) 

	def run(self):  


		while (self.running):
			# print(self.running)

			data = self.s.recv(1024)
			p = tcp_packet_pb2.TcpPacket()
			p.ParseFromString(data)
		

			if(p.type>4 and p.type<8):
				p = p.ErrPacket()
				p.ParseFromString(data)
				print("|> ERROR ", p.type, p.err_message)
				# return req
			elif (p.type == 0):
				p = p.DisconnectPacket()
				p.ParseFromString(data)
				
				print("<",p.player.name,"> --disconnected--")

			elif (p.type == 1):
				p = p.ConnectPacket()
				p.ParseFromString(data)
				
				print("<",p.player.name,"> --connected--: ")

			elif (p.type == 2):
				p = p.CreateLobbyPacket()
				p.ParseFromString(data)
				
				print("|> Lobby created. You may now connect to lobby: ", p.lobby_id)
           
			elif (p.type == 3):
				p = p.ChatPacket()
				p.ParseFromString(data)
		
				print("<",p.player.name,"> ", p.message)
				continue
			
			elif (p.type == 4):
				p = p.PlayerListPacket()
				p.ParseFromString(data)

				print("|>Start of list")
				for player in p.player_list:
					print("--Player ID:", player.id)
					print("       Name:", player.name)
				print("|>End of list")




#MAIN
HOST = '202.92.144.45'  # The server's hostname or IP address
PORT = 80        # The port used by the server


try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	listen = listenThread(s)
	listen.start()
except Exception as x:
	print("|> Error:", x)
	sys.exit()

packet = tcp_packet_pb2.TcpPacket()

type = opt()
while(True):
	if type == "1":
		Connect(s)
		type = "3"
		continue
	
	elif type == "2":
		Create_Lobby(s)

	elif type == "3":
		Chat(s, packet)

	elif type == "4":
		PlayerList(s)

	elif type == "0":
		listen.running = False
		Disconnect(s, packet)
		s.close()
		break
	# elif type == "5":
	# 	s.close()
	# 	print("|>Programm Terminated.")
	# 	listen.running = False
	# 	break;

	else:
		print ("Unknown option: Please enter a valid option. ")

	
	# print("\n\n---packet detsss---")
	# print(str(packet))
	type = opt()
