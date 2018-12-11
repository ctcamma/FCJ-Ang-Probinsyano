import socket
import select
import sys
from player import Player
from bullet import Bullet
from map import Map
import pygame
import json
import random

# Messages:
#  Client->Server
#   One or two characters. First character is the command:
#     c: connect
#     u: update position
#     d: disconnect
#   Second character only applies to position and specifies direction (udlr)
#
#  Server->Client
#   '|' delimited pairs of positions to draw the players (there is no
#     distinction between the players - not even the client knows where its
#     player is.

class GameServer(object):
  def __init__(self,gmap, port=9009, max_num_players=5):
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind to localhost - set to external ip to connect from other computers
    self.listener.bind(("0.0.0.0", port))
    self.read_list = [self.listener]
    self.write_list = []
    self.rand = 0
    self.stepsize = 5
    self.players = []
    self.spectators = []
    self.bullets = []
    self.bulletstate = []
    self.bulletpos = []
    self.bulletdirection = []
    self.bulletsource = []
    self.playerRects = []
    self.gmap = gmap
    self.p_width = 35
    self.p_height = 40
    self.gmap.initMapRects()
    self.TILE_SIZE = 50
    self.last_client = 0
    
  def do_movement(self, mv,idx,playerRects):
    pos = self.players[idx].pos
    if self.players[idx].walkCount == 7:
        self.players[idx].walkCount = 0
    if mv != self.players[idx].state:
        self.players[idx].walkCount = 0
        self.players[idx].count = 0

    pos_x, pos_y = self.players[idx].pos
    # print(self.gmap.obstacle_rects)
    self.players[idx].state = mv
    if mv == "u":
      new_rect = pygame.Rect( (pos_x, pos_y - self.stepsize), [self.p_width,self.p_height])
      if new_rect.collidelist(self.gmap.obstacle_rects) == -1:
        pos = (pos[0], max(0, pos[1] - self.stepsize))
    elif mv == "d":
      new_rect = pygame.Rect( (pos_x, pos_y + self.stepsize), [self.p_width,self.p_height])
      if new_rect.collidelist(self.gmap.obstacle_rects) == -1:
        pos = (pos[0], min(450, pos[1] + self.stepsize))
    elif mv == "l":
      new_rect = pygame.Rect( (pos_x - self.stepsize, pos_y), [self.p_width,self.p_height])
      if new_rect.collidelist(self.gmap.obstacle_rects) == -1:
        pos = (max(0, pos[0] - self.stepsize), pos[1])
    elif mv == "r":
      new_rect = pygame.Rect( (pos_x + self.stepsize, pos_y), [self.p_width,self.p_height])
      if new_rect.collidelist(self.gmap.obstacle_rects) == -1:
        pos = (min(700, pos[0] + self.stepsize), pos[1])


    # self.players[idx].rect = pygame.Rect( (pos_x, pos_y), [self.p_width,self.p_height])
    playerRects[idx] = pygame.Rect( (pos_x, pos_y), [self.p_width,self.p_height])
    self.players[idx].pos = pos
    # print(self.players[idx].pos)
    self.players[idx].count += 1
    if self.players[idx].count == 5:
        self.players[idx].count = 0
        self.players[idx].walkCount+=1
    return playerRects
    
  def run(self):
    while True:
      readable, writable, exceptional = (
        select.select(self.read_list, self.write_list, [])
      )
      for f in readable:
        if f is self.listener:
          msg, addr = f.recvfrom(1000)
          if len(msg) >= 1:
            msg = msg.decode("utf-8")
            cmd = msg[0]
            print(cmd)
            if cmd == "c":  # New Connection
              if len(self.players) == 0:
                self.rand = random.randrange(0,2)
              new_player = Player(addr,self.rand)
              # randomizing spawn point
              while True:
                row = random.randrange(0,10)
                col = random.randrange(0,15)
                if self.gmap.map[row][col] == 0:
                  new_player.pos = (col*self.TILE_SIZE,row*self.TILE_SIZE)
                  break
                else:
                  print()
              self.players.append(new_player)
              self.players[len(self.players)-1].number = self.last_client
              self.last_client += 1
              self.playerRects.append(pygame.Rect( (col*self.TILE_SIZE, row*self.TILE_SIZE), [self.p_width,self.p_height]))
            elif cmd == "u":  # Movement Update
              if len(msg) >= 2:
                for idx in range(0,len(self.players)):
                  if self.players[idx].addr == addr: 
                    self.playerRects = self.do_movement(msg[1],idx,self.playerRects)
            
            elif cmd == "s":
              for idx in range(0,len(self.players)):
                if self.players[idx].addr == addr:
                  self.players[idx].hasactivebullet=checkmapbullet(self.players[idx],self.bulletsource)
                  if(self.players[idx].hasactivebullet==True):
                    print()
                  else:
                    bullet = Bullet(self.players[idx].addr,self.players[idx].pos, self.players[idx].state)
                    bullet.start()
                    self.bullets.append(bullet)
                    self.bulletstate.append(bullet.state)
                    self.bulletpos.append(bullet.pos)
                    self.bulletdirection.append(bullet.direction)
                    self.bulletsource.append(bullet.source)
                    self.players[idx].hasactivebullet = True
            elif cmd == "d":  # Player Quitting TODO
              for idx in range(0,len(self.players)):
                if self.players[idx].addr == addr:
                  del self.players[idx]
                  del self.playerRects[idx]
                  break
            elif cmd == "w":
              client_num = len(self.players) + len(self.spectators)
              print(client_num)
              if client_num >= 3:
                for idx in range(0,len(self.players)):
                  self.players[idx].start = True
            else:
              a=1
        else:
          a=1
      
      send = []
      index = 0
      for bullet in self.bulletpos:
        bullet_collision = check_bullet_collision(self.bullets[index],self.bulletpos[index],self.bulletdirection[index],self.gmap,self.playerRects,self.players)
        if bullet_collision[0] == 0:
          self.bulletpos[index] = self.bullets[index].pos
          self.bulletstate[index] = self.bullets[index].state
        else:
            del self.bulletstate[index]
            del self.bulletsource[index]
            del self.bulletpos[index]
            del self.bulletdirection[index]
            del self.bullets[index]
            if len(bullet_collision) == 3:
              self.spectators.append(bullet_collision[0])
              self.players = bullet_collision[1]
              self.playerRects = bullet_collision[2]
        index += 1
        
      self.bulletstate, self.bulletsource, self.bulletpos, self.bulletdirection, self.bullets = checkactivebullet(self.bulletstate,self.bulletsource,self.bulletpos,self.bulletdirection,self.bullets)
      
      bpos_list = [bullet for bullet in self.bulletpos]
      bdirection_list = [bullet for bullet in self.bulletdirection]
      bsource_list = [bullet for bullet in self.bulletsource]
      spectator_list = [sl.__dict__ for sl in self.spectators]
      send.append(self.gmap.map)
      send.append(bpos_list)
      send.append(bdirection_list)
      send.append(bsource_list)
      send.append(spectator_list)
      if len(self.players)==1 and len(self.spectators) > 0:
        self.players[0].winner = True
        pl_list = [pl.__dict__ for pl in self.players]
        send.append(pl_list)
        send = json.dumps(send)
        for player in self.players:
          self.listener.sendto((send).encode(), player.addr)
        for spectator in self.spectators:
          self.listener.sendto((send).encode(), spectator.addr)
      else:
        pl_list = [pl.__dict__ for pl in self.players]
        send.append(pl_list)
        send = json.dumps(send)
        for player in self.players:
          self.listener.sendto((send).encode(), player.addr)
        for spectator in self.spectators:
          self.listener.sendto((send).encode(), spectator.addr)
      
      

def check_bullet_collision(self,pos,direction,gmap,playerRects,players):
    value = []
    if direction == 'u' or direction == 'd':
      new_rect = pygame.Rect( (pos[0], pos[1]), [19,7])
    else:
      new_rect = pygame.Rect( (pos[0], pos[1]), [7,19])
    index = 0
    collision = False
    for player in players:
      if self.source == player.addr:
        print()
      else:
        if new_rect.colliderect(playerRects[index]) == 0:
          print()
        else:
          collision = True
          break
      index+=1
    if new_rect.collidelist(gmap.obstacle_rects) == -1 and collision == False:
      value.append(0)
      return value
    else:
      num = 0
      for obs in gmap.obstacle_rects:
        if new_rect.colliderect(obs):
          pos = obs.topleft 
          num = pos 
          for idx in range(len(gmap.mapRects)):
            if gmap.mapRects[idx].topleft == pos:
              del gmap.mapRects[idx]
              gmap.updateObstacleRects()
              print(obs.left)
              print(obs.top)
              pos_x = obs.left//50
              pos_y = obs.top//50
              print(pos_x)
              print(pos_y)
              gmap.map[pos_y][pos_x] = 0
              break
          value.append(pos)
          return value
      index = 0
      for obs in playerRects:
        if new_rect.colliderect(obs):
          players[index].ingame = False
          value.append(players[index])
          del players[index]
          value.append(players)
          del playerRects[index]
          value.append(playerRects)
          break
        index+=1
      return value


def checkmapbullet(player,bulletsource):
  for bullet in bulletsource:
    if bullet == player.addr:
      return True
    else:
      continue
  return False

def checkactivebullet(bulletstate,bulletsource,bulletpos,bulletdirection,bullets):
  index = 0
  for bullet in bulletstate:
    if bullet == 0:
      del bulletstate[index]
      del bulletsource[index]
      del bulletpos[index]
      del bulletdirection[index]
      del bullets[index] 
    else:
      continue
  return bulletstate, bulletsource, bulletpos, bulletdirection, bullets

if __name__ == "__main__":
  gmap = Map()
  gmap.generateMap()
  print(gmap.map)
  g = GameServer(gmap)
  g.run()