#!/usr/bin/env python3
import sys 
sys.path.insert(0, '../proto')

#tcp packet for the char
import tcp_packet_pb2

import socket
from threading import Thread
import time
import tkinter as tk
import tkinter.messagebox as tkMessageBox

# def show_options():

class listenThread(Thread): 
	def __init__(self, socket): 
		Thread.__init__(self) 
		self.s = socket

		self.running = True
		self.waiting = False
		# print "[+] New server socket thread started for " + ip + ":" + str(port) 

	def run(self):  
		while (self.running):
			# print(self.running)
			if(self.waiting):
				print("thread is --listening--")
				try:
					data = self.s.recv(1024)
					p = tcp_packet_pb2.TcpPacket()
					p.ParseFromString(data)

					# print(p)
					if(p.type>4 and p.type<8):
							p = p.ErrPacket()
							p.ParseFromString(data)
							m = "|> Error " + str(p.type)
							m2 ="|" + p.err_message
							msg_list.insert(tk.END, "------------------------------------------------------------")
							msg_list.insert(tk.END, m)
							msg_list.insert(tk.END, m2)
							msg_list.insert(tk.END, "------------------------------------------------------------")
						
					elif (p.type == 0):
						print("---disconnection packet received")
						p = p.ConnectPacket()
						p.ParseFromString(data)
						m = "<"+p.player.name+"> ---disconnected---"
						msg_list.insert(tk.END, m)

					elif (p.type == 1):
						print("---connection packet received")
						p = p.ConnectPacket()
						p.ParseFromString(data)
						m = "<"+p.player.name+"> ---connected---"
						msg_list.insert(tk.END, m)

					elif (p.type == 2):
						print("--create packet received")
						p = p.CreateLobbyPacket()
						p.ParseFromString(data)
						m = "|> Lobby Created"
						m2 = "|lobby id : "+p.lobby_id 
						msg_list.insert(tk.END, "------------------------------------------------------------")
						msg_list.insert(tk.END, m)
						msg_list.insert(tk.END, m2)
						msg_list.insert(tk.END, "------------------------------------------------------------")

					elif (p.type == 3):
						p = p.ChatPacket()
						p.ParseFromString(data)
						if (p.message != ""):
							m = "<" + p.player.name + "> " + p.message
							msg_list.insert(tk.END, m)

					elif (p.type == 4):
						p = p.PlayerListPacket()
						p.ParseFromString(data)

						msg_list.insert(tk.END, "------------------------------------------------------------")
						msg_list.insert(tk.END, "|> Player list")
						i=0
						for player in p.player_list:
							i = i+1
							m = str(i)+". "+player.name
							msg_list.insert(tk.END, m)
						msg_list.insert(tk.END, "------------------------------------------------------------")
				except Exception as x:
						self.running = False
						print("--")

def Connect(s, player_name, lobby_id):
	print("---connecting---")
	# initialization of the request connect packet
	req = tcp_packet_pb2.TcpPacket.ConnectPacket()
	req.type = 1
	req.player.name = player_name
	req.lobby_id = lobby_id

	s.sendall(req.SerializeToString())

def Chat(s, p, message):    
	# Initialization of the request chat packet
	req = tcp_packet_pb2.TcpPacket.ChatPacket()
	req.type = 3

	try:
		req.player.CopyFrom(p.player)
		req.lobby_id = p.lobby_id 
	except Exception as x:
		print("")
	req.message = message

	s.sendall(req.SerializeToString())

def Create_Lobby(s, max_no):
	#initialization of the Create Lobby Packet
	req = tcp_packet_pb2.TcpPacket.CreateLobbyPacket()
	req.type = 2
	req.max_players = int(max_no)

	print("..create packet sending...")
	s.sendall(req.SerializeToString())

def PlayerList(s):
	req = tcp_packet_pb2.TcpPacket.PlayerListPacket()
	req.type = 4

	s.sendall(req.SerializeToString())

def Disconnect(s, p):
	req = tcp_packet_pb2.TcpPacket.DisconnectPacket()
	req.type = 0

	try:
		req.player.CopyFrom(p.player)
	except Exception as x:
		print(" ")

	s.sendall(req.SerializeToString())
	listen.running= False


def msg_checker(event=None):
	global p,s,listen

	m = msg.get()
	t = tcp_packet_pb2.TcpPacket()
	sm = m.split(" ")
	# print(sm[0], len(sm))
	
	listen.waiting = True

	if(sm[0] == "/connect"):
		if(len(sm) == 3):
			Connect(s, sm[1], sm[2])

			p = t.ConnectPacket()
			p.type = 1
			p.player.name = sm[1]
			p.lobby_id = sm[2]

		else:
			msg_list.insert(tk.END, "|Error usage of")
			msg_list.insert(tk.END, "/connect <name> <lobby_id>")

	elif (sm[0] == "/create"):
		if(len(sm) == 2):
			Create_Lobby(s, sm[1])
		else: 
			msg_list.insert(tk.END, "|Error usage of")
			msg_list.insert(tk.END, "/create <max_player_number>")

	elif (sm[0] == "/players"):
		PlayerList(s)

	elif (sm[0] == "/disconnect"):
		Disconnect(s, p)
		s.close() 
		# try:
		# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 	s.connect((HOST, PORT))
		# 	#start of the listening thread
		# 	listen = listenThread(s)
		# 	listen.start()
		# except Exception as x:
		# 	print("|Error ", x)
		# 	sys.exit()
		listen.waiting = False
	
	elif (sm[0] == "/create"):
		Create_Lobby(s)

	elif ("/" in sm[0]):
		msg_list.insert(tk.END, "|Error no command found")
	
	else: #Chat Packets
		Chat(s, p, m)

	#clears out the text field
	msg.set("")
	# listen.waiting = False

def closing(event=None):
	"""This function is to be called when the window is closed."""
	listen.running = False
	msg.set("/disconnect")	
	main_window.quit()

def show_game_help():
	opt = "this is the game help?"
	tkMessageBox.askquestion("Game help", opt)

#initialization of the tkinter
main_window = tk.Tk()
main_window.title("FCJ: Ang Prbonsyano")

#frames are container of the widgets
chat_frame = tk.Frame(main_window, bg="blue", height=750, width=300)

game_frame = tk.Frame(main_window, bg="brown", height=750, width=750)

msgs_frame = tk.Frame(chat_frame, bg="blue")

msg = tk.StringVar()
msg.set("Type your messages here.")

#widget - string field for the messages
# scrollbar = tk.Scrollbar(msgs_frame) 
msg_list = tk.Listbox(msgs_frame, height=30, width=30)
# msg_list = tk.Listbox(msgs_frame, height=30, width=30,yscrollcommand=scrollbar.set)

chat_help_text = tk.Text(msgs_frame, bg="cyan")
opt = "\nCHAT OPTIONS\n-create a lobby\n /create <max_no_of_players>\n-connect to a lobby\n /connect <player_name> <lobby_id>\n-show players in the lobby\n /players\n-disconnect from the lobby\n /disconnect"
chat_help_text.insert(tk.INSERT, opt)
chat_help_text.config(state=tk.DISABLED) 
chat_help_text.tag_add("h", "1.0", "1.12")
chat_help_text.tag_config("h", background="black", foreground="cyan")


game_help_b = tk.Button(chat_frame, text="GAME HELP", command=show_game_help)
# chat_option = tk.Text(msgs_frame, bg="cyan", height=10, width=40)

msg_field = tk.Entry(msgs_frame, textvariable=msg)
msg_field.bind("<Return>", msg_checker)

#packing 

# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack()
msg_list.pack()
msg_field.pack()
chat_help_text.pack()
# game_help_b.pack()
# chat_option.pack()

msgs_frame.place(bordermode=tk.OUTSIDE, height=700, width=300)
chat_frame.pack(side=tk.LEFT)
game_frame.pack( side=tk.LEFT )

#START
HOST = '202.92.144.45'  # The server's hostname or IP address
PORT = 80        # The port used by the server

p = tcp_packet_pb2.TcpPacket()
connected = True
#connecting to the server through sockets
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	#start of the listening thread
	listen = listenThread(s)
	listen.start()
except Exception as x:
	print("|Error ", x)
	sys.exit()

# print(s)
main_window.protocol("WM_DELETE_WINDOW", closing)
main_window.mainloop()
