#dot
import numpy as np
import pygame
import constants
import time

display_width = constants.display_width
display_height = constants.display_height

dot_width = constants.dot_width
dot_height = constants.dot_height

white = constants.white
black = constants.black
red   = constants.red

max_moves = constants.max_moves

#goal
x_goal = constants.x_goal
y_goal = constants.y_goal

f_vis = constants.forward_vision 
s_vis = int(f_vis/2)   #side vision

class Dot:

	def __init__(self,x,y,Theta1,Theta2, environment):
		self.x = x
		self.y = y
		self.Theta1 = Theta1
		self.Theta2 = Theta2
		self.alive = True
		self.moves = 0
		self.env = environment
		self.velocity = 0
		

	def move(self):

		if self.alive == True:
			x_change = 0
			y_change = 0

			directional_input = self.look()
			positional_input = np.array([self.x,self.y])
			inputs = np.hstack((directional_input.ravel(),positional_input.ravel()))
			#inputs = self.look().ravel()
			action = self.think(inputs)
			
			if action[0] == 1:
				x_change = -1  #moving left
				self.velocity = 4
			elif action[1] == 1:
				x_change = 1  #moving right
				self.velocity = 2
			elif action[2] == 1:
				y_change = -1 #moving upwards
				self.velocity = 3
			elif action[3] ==1:
				y_change = 1  #moving downwards
				self.velocity = 1

			#updating position
			self.x += x_change
			self.y += y_change

			#updating no. of moves
			self.moves += 1
	
	
	#brain part
	def look(self):
		x, y = self.x, self.y
		inputs = self.get_inputs(x, y)
		return inputs
	
	def get_inputs(self,x,y):
		vel = self.velocity
		if vel == 1:
			return self.env[y:y+f_vis, x-s_vis:x+s_vis]
		elif vel == 3:
			return self.env[y-f_vis:y, x-s_vis:x+s_vis]
		elif vel == 2:
			return self.env[x:x+f_vis, y-s_vis:y+s_vis]
		elif vel == 4:
			return self.env[x-f_vis:x, y-s_vis:y+s_vis]
		else:
			return self.env[x-s_vis:x+s_vis, y-s_vis:y+s_vis]

	def think(self, inputs):
		output = forward_propagation(inputs,self.Theta1, self.Theta2)
		return self.take_action(output)

	def take_action(self,ouput):
		action = np.zeros(ouput.shape[0])
		max = np.argmax(ouput)
		action[max] = 1

		return action

	def draw(self,gameDisplay):
		if self.alive:
			pygame.draw.rect(gameDisplay, white, [self.x, self.y , constants.dot_width, constants.dot_height])
		else:
			pygame.draw.rect(gameDisplay, red, [self.x, self.y , constants.dot_width, constants.dot_height])
	
	#life and death
	def isAlive(self):
		return self.alive

	def kill(self, death_type):
		fitness = self.cal_fitness(self.x, self.y )
		
		if death_type == 1:  #it's a crime to die on boundaries
			fitness -= 0.01
		
		self.alive = False
		return fitness

	def cal_fitness(self, x , y):
		distance = (x - x_goal)**2 + (y - y_goal)**2
		fitness = 1000/int(distance)
		return fitness

	#getters
	def get_moves(self):
		return self.moves

	def get_position(self):
		return self.x, self.y
	
	def get_velocity():
		return self.velocity
	
	
def forward_propagation(X, Theta1, Theta2):
    a_1 = np.hstack((np.ones((1)),X))         # added bias to input layer
    z_2 = np.dot(Theta1,a_1)
    a_2 = np.hstack((np.ones(1), sigmoid(z_2)))  # added bias to hidden layer
    z_3 = np.dot(Theta2, a_2)
    a_3 = sigmoid(z_3)

    return a_3

def sigmoid(z):
	return 1/(1 + np.exp(-z))

