import pygame
import threading
import time
from threading import Thread

class Bullet(Thread):
    (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)
    (DESTROYED, ACTIVE) = range(2)
    def __init__(self, addr, pos, state):
        Thread.__init__(self)
        self.running = True
        
        self.direction = state
        self.damage = 100
        self.state = self.ACTIVE
        self.source = addr
        # 1-regular everyday normal bullet
        # 2-can destroy steel
        self.power = 1

        # position is addr's top left corner, so we'll need to
        # recalculate a bit. also rotate image itself.
        if self.direction == 'u':
            self.rect = pygame.Rect(pos[0], pos[1]-24, 6, 8)
            self.pos = (pos[0],pos[1]-24)
        elif self.direction == 'r':
            self.rect = pygame.Rect(pos[0]+16, pos[1]+16, 8, 6)
            self.pos = (pos[0]+16,pos[1]+16)
        elif self.direction == "d":
            self.rect = pygame.Rect(pos[0],pos[1]+32, 6, 8)
            self.pos = (pos[0],pos[1]+32)
        elif self.direction == 'l':
            self.rect = pygame.Rect(pos[0]-20, pos[1]+16, 8, 6)
            self.pos = (pos[0]-20,pos[1]+16)
        self.speed = 5

    # def draw(self,surface):
    #     """ draw bullet """
    #     screen.blit(self.image, (self.pos[0], self.pos[1]))
    #     print("x:",self.pos[0]," y: ",self.pos[1])

    def destroy(self):
        self.state = self.DESTROYED

    def run(self):
        bulletupdate(self,self.direction)

    # def update(self):
    #     """ move bullet """
    #     collided = False
    #     for obs in obstacle_rects:
    #         if self.rect.colliderect(obs.rect):
                
    #             self.destroy()
    #             collided = True
    #             pos = obs.rect.topleft
    #             for idx in range(len(mapr)):
    #                 if mapr[idx].rect.topleft == pos:
    #                     print('removed')
    #                     mapr[idx] = Obstacle((mapr[idx].rect.left, mapr[idx].rect.top), GRASS, 'grass.png')
    #                     update_rects()
    #     if not collided:    
    #         if self.direction == self.DIR_UP:
    #             self.rect.topleft = [self.rect.left, self.rect.top - self.speed]

    #         elif self.direction == self.DIR_RIGHT:
    #             self.rect.topleft = [self.rect.left + self.speed, self.rect.top]

    #         elif self.direction == self.DIR_DOWN:
    #             self.rect.topleft = [self.rect.left, self.rect.top + self.speed]

    #         elif self.direction == self.DIR_LEFT:
    #             self.rect.topleft = [self.rect.left - self.speed, self.rect.top]
        

def bulletupdate(thread,direction):
    while((thread.pos[0] > 0 and thread.pos[0] < 750) and (thread.pos[1] > 0 and thread.pos[1] < 500)):
        time.sleep(0.01)
        if direction == 'u':
            thread.pos = (thread.pos[0], thread.pos[1] - thread.speed)
        elif direction == 'r':
            thread.pos = (thread.pos[0] + thread.speed, thread.pos[1])
        elif direction == 'd':
            thread.pos = (thread.pos[0], thread.pos[1] + thread.speed)
        elif direction == 'l':
            thread.pos = (thread.pos[0] - thread.speed, thread.pos[1])
    thread.destroy()