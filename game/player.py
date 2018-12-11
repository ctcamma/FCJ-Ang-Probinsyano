import pygame


class Player(pygame.sprite.Sprite):  # represents the bird, not the game
    def __init__(self,addr,rand):
        pygame.sprite.Sprite.__init__(self)
        """ The constructor of the class """
        # self.image = pygame.image.load("1.png")

        self.addr = addr
        self.number = 0
        self.map_style= rand
        self.height = 52
        self.width = 35
        self.x = 0
        self.y = 0
        self.pos =(self.x,self.y)
        # self.rect = self.current.get_rect()
        self.state = 'd'
        self.count = 0
        self.hasactivebullet = False    
        self.walkCount = 0
        self.start = False
        # self.rect = pygame.Rect( (self.x, self.y), [self.width,self.height])

    # def fire(self):
    #     global screen, bullets
    #     print()
    #     bullet = Bullet(self,self.x,self.y, self.direction)
    #     bullet.start()
    #     bullets.append(bullet)
    #     self.hasactivebullet = True
    #     return True

    # def handle_keys(self,obstacle_rects):
    #     # global now, lasttime
    #     """ Handles Keys """
    #     key = pygame.key.get_pressed()
    #     dist = 3 # distance moved in 1 frame, try changing it to 5
    #     self.prev_x,self.prev_y = self.x,self.y
    #     if key[pygame.K_DOWN]: # down key
    #         new_rect = pygame.Rect( (self.x, self.y+dist), [self.width,self.height-10])
    #         self.animate('front')
    #         self.direction = self.DIR_DOWN
    #         if new_rect.collidelist(obstacle_rects) == -1 and self.y+dist < 450:
    #             self.y += dist # move down
    #     elif key[pygame.K_UP]: # up key
    #         new_rect = pygame.Rect( (self.x, self.y-dist), [self.width,self.height-10])
    #         self.animate('back')
    #         self.direction = self.DIR_UP
    #         if new_rect.collidelist(obstacle_rects) == -1 and self.y-dist > 0:
    #             self.y -= dist # move up
    #     elif key[pygame.K_LEFT]: # right key
    #         new_rect = pygame.Rect( (self.x-dist, self.y), [self.width,self.height-10])
    #         self.animate('left')
    #         self.direction = self.DIR_LEFT
    #         if new_rect.collidelist(obstacle_rects) == -1 and self.x-dist > 0:
    #             self.x -= dist # move right
    #     elif key[pygame.K_RIGHT]: # left key
    #         new_rect = pygame.Rect( (self.x+dist, self.y), [self.width,self.height-10])
    #         self.animate('right')
    #         self.direction = self.DIR_RIGHT
    #         if new_rect.collidelist(obstacle_rects) == -1 and self.x+dist < 750:
    #             self.x += dist # move left
                
        # elif key[pygame.K_SPACE]: # space key
        #     pressed = pygame.key.get_pressed()
        #     if(pressed[pygame.K_SPACE] and (now-lasttime)<0.2):
        #         print("x:",self.x," y: ",self.y)
        #     else:
        #         lasttime = now
        #         self.hasactivebullet=checkmapbullet(self)
        #         if(self.hasactivebullet==True):
        #             print()
        #         else:    
        #             self.fire()

            

    # def draw(self, surface):
    #     """ Draw on surface """
    #     # blit yourself at your current position
    #     surface.blit(self.current, (self.x, self.y))
    #     self.rect = pygame.Rect( (self.x, self.y), [self.width,self.height])
        # self.rect.fill(pygame.Color('steelblue2'))
    # def animate(self, direction):
    #     if self.walkCount == 8:
    #         self.walkCount = 0
    #     if direction != self.state:
    #         self.walkCount = 0
    #         self.count = 0

    #     self.state = direction 

    #     if(direction == DIR_UP):
    #         self.current = self.front_frames[self.walkCount]
    #     elif(direction == DIR_DOWN):
    #         self.current = self.back_frames[self.walkCount]
    #     elif(direction == 'right'):
    #         self.current = self.right_frames[self.walkCount]
    #     elif(direction == 'left'):
    #         self.current = self.left_frames[self.walkCount]
        
    #     self.count += 1
    #     if self.count == 5:
    #         self.count = 0
    #         self.walkCount+=1