import pygame
import pygame.locals
import socket
import select
import random
import time
import os
import json
from map import Map
from sprite import Sprite
# os.en

class GameClient(object):
  def __init__(self, addr="127.0.0.1", serverport=9009):
    self.clientport = random.randrange(8000, 8999)
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to localhost - set to external ip to connect from other computers
    self.conn.bind((addr, self.clientport))
    self.addr = addr
    self.number = 0
    self.serverport = serverport
    self.read_list = [self.conn]
    self.write_list = []
    self.ingame = True
    self.winner = False
    self.endgame = False
    self.start = False
    # self.player = Player((self.addr,self.serverport))
    self.setup_pygame()
  
  def setup_pygame(self, width=750, height=500):
    pygame.init()
    pygame.display.list_modes()

    self.screen = pygame.display.set_mode((width, height))
    self.bg_surface = pygame.image.load("bg.png").convert()
    # self.tree_image = pygame.image.load("sprite.png").convert_alpha()
    self.tree_image = pygame.image.load("tree.png").convert_alpha() 
    self.bullet_image = pygame.image.load("bullet.png").convert_alpha()
    self.lose_image = pygame.image.load("lose.jpg").convert_alpha()
    self.win_image = pygame.image.load("win.png").convert_alpha()
    self.wait_image = pygame.image.load("waiting.png").convert_alpha()
    # self.tree_image = pygame.image.load("grass.png").convert_alpha()  
    self.TILE_SIZE = 50
    
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.locals.QUIT,
                              pygame.locals.KEYDOWN])
    pygame.key.set_repeat(50, 50)

  def run(self):
    running = True
    clock = pygame.time.Clock()
    tickspeed = 30
    clienthasbullet = False
    try:
      # Initialize connection to server
      self.conn.sendto(bytes("c","utf-8"), (self.addr, self.serverport))


      while running:
        clock.tick(tickspeed)
        
        # select on specified file descriptors
        readable, writable, exceptional = (
            select.select(self.read_list, self.write_list, [], 0)
        )
        for f in readable:
          if f is self.conn:
            msg, addr = f.recvfrom(5000)

            
            x,y = 0,0
            data = json.loads(msg.decode())
            # print(players[0]['state'])
            game_map = data[0]
            players = data[5]


            if players[0]["map_style"] == 0:
              self.bg_surface =  pygame.image.load("bg.png").convert()
              self.obs_image =  pygame.image.load("tree.png").convert()
            elif players[0]["map_style"] == 1:
              self.bg_surface =  pygame.image.load("sand.png").convert()
              self.obs_image =  pygame.image.load("cactus.png").convert()
              
            self.screen.blit(self.bg_surface, (0,0))  # Draw the background

            for row in game_map:
              for tile in row:
                if tile == 1:
                  self.screen.blit(self.obs_image, (x,y))
                x += self.TILE_SIZE
              x = 0
              y += self.TILE_SIZE
            
            bullets = data[1]
            
            bulletdirection = data[2]
            index = 0
            for bl in bullets:
              if bulletdirection[index] == 'u':
                self.screen.blit(self.bullet_image,(bl[0],bl[1]))
              elif bulletdirection[index] == 'd':
                self.screen.blit(pygame.transform.rotate(self.bullet_image, 180),(bl[0],bl[1]))
              elif bulletdirection[index] == 'r':
                self.screen.blit(pygame.transform.rotate(self.bullet_image, 270),(bl[0],bl[1]))
              elif bulletdirection[index] == 'l':
                self.screen.blit(pygame.transform.rotate(self.bullet_image, 90),(bl[0],bl[1]))
              

            bulletsource = data[3]
            clienthasbullet=False
            for bl in bulletsource:
              if bl == [self.addr, self.clientport]:
                clienthasbullet=True    
                break
              else:
                clienthasbullet=False

            spectators = data[4]
            for sl in spectators:
              if self.clientport == sl['addr'][1]:
                self.ingame = False

            
            for pl in players: 
              self.number = pl['number']
              sprite = Sprite(self.number)
              if self.clientport == pl['addr'][1]:
                self.start = pl['start']
                
                # self.start = pl['start']
                if len(players) == 1 and len(spectators) > 0:
                  print("Winner Winner Chicken Dinner")
                  self.endgame = True
              self.screen.blit(sprite.updateFrame(pl['state'],pl['walkCount']), pl['pos'])


        if self.ingame == True or self.start == True:
          for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
              running = False
              break
            elif event.type == pygame.locals.KEYDOWN:
              if event.key == pygame.locals.K_UP:
                self.conn.sendto("uu".encode("utf-8"), (self.addr, self.serverport))
              elif event.key == pygame.locals.K_DOWN:
                self.conn.sendto("ud".encode("utf-8"), (self.addr, self.serverport))
              elif event.key == pygame.locals.K_LEFT:
                self.conn.sendto("ul".encode("utf-8"), (self.addr, self.serverport))
              elif event.key == pygame.locals.K_RIGHT:
                self.conn.sendto("ur".encode("utf-8"), (self.addr, self.serverport))
              elif event.key == pygame.locals.K_SPACE:
                self.conn.sendto("s".encode("utf-8"), (self.addr, self.serverport))
              pygame.event.clear(pygame.locals.KEYDOWN)
        
        if self.ingame == False:
          self.screen.blit(self.bg_surface, (0,0))
          self.screen.blit(self.lose_image, (0,0))
        
        if self.endgame == True:
          self.screen.blit(self.bg_surface, (0,0))
          self.screen.blit(self.win_image, (0,0))

        if clienthasbullet == True:
          time.sleep(0.000001)
          self.conn.sendto("a".encode("utf-8"), (self.addr, self.serverport))
        
        if self.start == False:
          self.screen.fill((0,0,0))
          self.screen.blit(self.wait_image, (0,0))
          self.conn.sendto("w".encode("utf-8"), (self.addr, self.serverport))
        
        pygame.display.update()
    finally:
      self.conn.sendto("d".encode("utf-8"),(self.addr, self.serverport))


if __name__ == "__main__":
  g = GameClient()
  g.run()
