#Snake class
import pygame

class Snake:

	red = (220,0,0)
	white = (255,255,255)
	def __init__(self,width,height,x_start,y_start,length=1):
		self.snake_width = width
		self.snake_height = height
		self.length = length
		self.X = [x_start]
		self.Y = [y_start]
		for i in range(1,length):
			self.X.append(x_start-width)
			self.Y.append(y_start)
		self.x_change = 0
		self.y_change = 0

	def draw(self,gameDisplay):
		for i in range(len(self.X)):
			pygame.draw.rect(gameDisplay, self.__class__.red if i==0 else self.__class__.white, 
				[self.X[i], self.Y[i], self.snake_width, self.snake_height])

	def eat_food(self):
		self.X.append(0)
		self.Y.append(0)
		self.length += 1

	def move(self,event):
		
		x_change = 0
		y_change = 0

		if event.type == pygame.KEYDOWN:
				
			if event.key == pygame.K_LEFT:
				x_change = -self.snake_width
				y_change = 0
			elif event.key == pygame.K_RIGHT:
				x_change = self.snake_width
				y_change = 0
			elif event.key == pygame.K_UP:
				y_change = -self.snake_height
				x_change = 0
			elif event.key == pygame.K_DOWN:
				y_change = self.snake_height
				x_change = 0

			self.x_change,self.y_change = x_change,y_change

	def update_position(self):
		a = len(self.X)
		for i in range(a-1,0,-1):
			self.X[i] = self.X[i-1]
			self.Y[i] = self.Y[i-1]
		
		self.X[0] = self.X[0] + self.x_change
		self.Y[0] = self.Y[0] + self.y_change
		
		for i in range(1,a):
			if self.X[0] == self.X[i] and self.Y[0] == self.Y[i]:
				self.kill()
				return True

		return False

	def head(self):
		return self.X[0], self.Y[0]

	def kill(self):
		print('bye!')