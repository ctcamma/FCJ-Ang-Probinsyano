import pygame
import random

class Obstacle(pygame.Rect):
    def __init__(self, left,top, type, width = 50, height = 50):
        pygame.Rect.__init__(self, left, top, width, height)
        # self.image = pygame.image.load(image_file)
        # self.rect = self.image.get_rect()
        # self.rect.left, self.rect.top = location
        self.type = type

class Map(object):
    (TREE, GRASS) = range(2)
    def __init__(self):
        # 15 x 10 map     
        self.map = []
        self.TILE_SIZE = 50
        self.map_width = 15
        self.map_height = 10
        self.tree_image= pygame.image.load('tree.png')
        # self.grass_image= pygame.image.load('grass.png')
        self.x,self.y = 0,0
        self.mapRects = []
        self.obstacle_rects = []

    def generateMap(self):    
        map_cols = []
        for x in range(0,10):
            map_rows = []
            for y in range(0,15):
                map_rows.append(random.randint(0,3))
            map_cols.append(map_rows)
        self.map = map_cols

    def initMapRects(self):
        for row in self.map:
            for data in row:
                if data == 1:
                    self.mapRects.append(Obstacle(self.x, self.y, self.TREE))

                self.x += self.TILE_SIZE
            self.x=0
            self.y += self.TILE_SIZE
          
        self.updateObstacleRects()

    def updateObstacleRects(self):
        self.obstacle_rects.clear()
        for tile in self.mapRects:
            if tile.type == self.TREE:
                self.obstacle_rects.append(tile)

