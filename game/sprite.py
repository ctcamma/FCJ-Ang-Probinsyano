import pygame

class Sprite(object):
	"""docstring for ClassName"""
	def __init__(self,index):

		self.offset = 10
		self.width = 35
		self.height  = 52
		self.right_sheet = [pygame.image.load('blue_right.png').convert_alpha(),pygame.image.load('red_right.png').convert_alpha(),pygame.image.load('green_right.png').convert_alpha(),pygame.image.load('yellow_right.png').convert_alpha()]
		self.left_sheet = [pygame.image.load('blue_left.png').convert_alpha(),pygame.image.load('red_left.png').convert_alpha(),pygame.image.load('green_left.png').convert_alpha(),pygame.image.load('yellow_left.png').convert_alpha()]
		self.front_sheet = [pygame.image.load('blue_front.png').convert_alpha(),pygame.image.load('red_front.png').convert_alpha(),pygame.image.load('green_front.png').convert_alpha(),pygame.image.load('yellow_front.png').convert_alpha()]
		self.back_sheet = [pygame.image.load('blue_back.png').convert_alpha(),pygame.image.load('red_back.png').convert_alpha(),pygame.image.load('green_back.png').convert_alpha(),pygame.image.load('yellow_back.png').convert_alpha()]

		self.sheet_width, self.sheet_height = self.right_sheet[index].get_size()
		self.front_frames = [self.front_sheet[index].subsurface(pygame.Rect(self.width*i+self.offset,0, self.width-self.offset,self.height)) for i in range(0,8)]
		self.back_frames = [self.back_sheet[index].subsurface(pygame.Rect(self.width*i+self.offset,0, self.width-self.offset,self.height)) for i in range(0,8)]
		self.right_frames = [self.right_sheet[index].subsurface(pygame.Rect(self.width*i,0, self.width,self.height)) for i in range(0,8)]
		self.left_frames = [self.left_sheet[index].subsurface(pygame.Rect(self.width*i,0, self.width,self.height)) for i in range(0,8)]
		self.current = self.front_frames[0]

	def updateFrame(self, direction, idx):
		if(direction == 'd'):
			return self.front_frames[idx]
		elif(direction == 'u'):
			return self.back_frames[idx]
		elif(direction == 'r'):
			return self.right_frames[idx]
		elif(direction == 'l'):
			return self.left_frames[idx]

