#Snake class
import pygame
import numpy as np 
import constants
import random
import time
from collections import deque 

#screen
display_width = constants.display_width
display_height = constants.display_height

#colors 
red = constants.red
white = constants.white

#snake
head_width = constants.head_width
head_height = constants.head_height

white = constants.white
black = constants.black
red   = constants.red
blue = constants.blue
orange = constants.orange

#food 
food_height = constants.food_height
food_width = constants.food_width

class Snake:

	def __init__(self,x_start,y_start, Theta1, Theta2):
		self.length = 4
		
		self.random_initialise_snake(x_start, y_start)  #snake's starting positions
		#non random initiation
		#self.X = deque([x_start,x_start,x_start,x_start])
		#self.Y = deque([y_start,y_start-head_height,y_start-head_height*2, y_start-head_height*3])	
		
		self.alive = True
		self.moves = 0
		self.velocity = 0
		#brain parts
		self.Theta1 = Theta1
		self.Theta2 = Theta2
		
	def random_initialise_snake(self, x_start, y_start):
		#initialise the snake in random orientation
		a = random.randint(0,3)
		if a==1:
			self.X = deque([x_start,x_start,x_start,x_start])
			self.Y = deque([y_start,y_start-head_height,y_start-head_height*2, y_start-head_height*3])
		elif a==2:
			self.X = deque([x_start,x_start-head_width,x_start-head_width*2, x_start-head_width*3])
			self.Y = deque([y_start,y_start,y_start,y_start])
		elif a==3:
			self.X = deque([x_start,x_start,x_start,x_start])
			self.Y = deque([y_start,y_start+head_height,y_start+head_height*2, y_start+head_height*3])
		else:
			self.X = deque([x_start,x_start+head_width,x_start+head_width*2, x_start+head_width*3])
			self.Y = deque([y_start,y_start,y_start,y_start])
		
	def draw(self,gameDisplay):
		if self.alive:
			for i in range(len(self.X)):
				pygame.draw.rect(gameDisplay, blue if i==0 else white, 
					[self.X[i], self.Y[i], head_width, head_height])
		#comment this to see stop seeing the snakes which are killed
		else:
			for i in range(len(self.X)):
				pygame.draw.rect(gameDisplay, red if i==0 else orange, 
					[self.X[i], self.Y[i], head_width, head_height])

	def eat_food(self,x_food,y_food):
		self.X.appendleft(x_food) 
		self.Y.appendleft(y_food)
		self.length += 1

	def move(self, x_food, y_food):
		
		if self.alive:
			x_change = 0
			y_change = 0

			vision = self.look(x_food, y_food)
			
			action = self.think(vision.ravel())
			
			if action[0] == 1:
				x_change = -head_width  #moving left
				self.velocity = 4
			elif action[1] == 1:
				x_change = head_width   #moving right
				self.velocity = 2
			elif action[2] == 1:
				y_change = -head_height #moving upwards
				self.velocity = 3
			elif action[3] ==1:
				y_change = head_height  #moving downwards
				self.velocity = 1

			# updating snake body position
			length = self.length -1
			for i in range(length,0,-1):
				self.X[i] = self.X[i-1]
				self.Y[i] = self.Y[i-1]

			#updating head position
			self.X[0] = self.X[0] + x_change
			self.Y[0] = self.Y[0] + y_change
			
			#updating no. of moves
			self.moves += 1

	
	def think(self, inputs):
		output = forward_propagation(inputs,self.Theta1, self.Theta2)
		return self.take_action(output)

	def take_action(self,ouput):
		action = np.zeros(ouput.shape[0])
		max = np.argmax(ouput)
		action[max] = 1

		return action

	def bit_itself(self):
		length = self.length
		for i in range(1,length):
			if self.X[0] == self.X[i] and self.Y[0] == self.Y[i]:
				return True

	def is_On_body(self,y_check, x_check):
		for x,y in zip(self.X,self.Y):
			if x==x_check and y==y_check:
				return True
		return False

		return False

	def head_pos(self):
		return self.X[0], self.Y[0]

	def kill(self,gen):
		fitness = self.cal_fitness(gen)
		self.alive = False
		return fitness
	
	def is_Alive(self):
		return self.alive

	def cal_fitness(self, gen):
		moves = self.moves
		#this fitness function barely works, have to come up with a better one
		if gen<20:
			fitness = (moves)*(moves) + 50*pow(2, self.length-4)
		else:
			fitness = moves*pow(2, self.length -4)
		return fitness
		
	
	#getters
	def get_moves(self):
		return self.moves

	def get_max_moves(self,gen):
		if gen<20:
			return 200
		else:
			return 500  # more moves
	
	def get_velocity(self):
		return self.velocity
	
	def look(self, x_food, y_food):

		#we will look in all directions in a clockwise manner

		#look up
		up         = self.lookInDirection(x_food, y_food ,y=-1, x=0) 
		#look up/right
		up_right   = self.lookInDirection(x_food, y_food ,y=-1, x=1)
		#look right
		right      = self.lookInDirection(x_food, y_food ,y=0, x=1)
		#look down/right
		down_right = self.lookInDirection(x_food, y_food ,y=1, x=1)
		#look down
		down       = self.lookInDirection(x_food, y_food ,y=1, x=0)
		#look down/left
		down_left  = self.lookInDirection(x_food, y_food ,y=1, x=-1)
		#look left
		left       = self.lookInDirection(x_food, y_food ,y=0, x=-1)
		#look up/lefts
		up_left    = self.lookInDirection(x_food, y_food ,y=-1, x=-1)
	
		return np.hstack((up,up_right,right, down_right, down, down_left, left, up_left))
	
	def lookInDirection(self, x_food, y_food ,y, x):
		food_found = 0
		tail_found = 0
		wall_distance = 1 #starting with 1 as it is the max value it can take
						 #input to the neural net is 1/wall_distance

		curr_x, curr_y = self.head_pos()
		check_x, check_y = curr_x + x*food_width, curr_y + y*food_height #moving one step in the looking direction

		while check_y>0 and check_y<display_height and check_x>0 and check_x<display_width:

			if food_found==0 and (check_y==y_food and check_x==x_food):
				food_found = 1
			
			if tail_found==0 and (self.is_On_body(check_y,check_x)):
				tail_found = 1
	 
			check_y += y*food_height
			check_x += x*food_height
			
			wall_distance += 1

		saw = np.array([1/wall_distance, food_found, tail_found])
		
		return saw


def forward_propagation(X, Theta1, Theta2):
    a_1 = np.hstack((np.ones((1)),X))         # added bias to input layer
    z_2 = np.dot(Theta1,a_1)
    a_2 = np.hstack((np.ones(1), sigmoid(z_2)))  # added bias to hidden layer
    z_3 = np.dot(Theta2, a_2)
    a_3 = sigmoid(z_3)

    return a_3

def sigmoid(z):
	return 1/(1 + np.exp(-z))