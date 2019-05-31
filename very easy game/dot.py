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

class Dot:

	def __init__(self,x,y,Theta1,Theta2, game_matrix):
		self.x = x
		self.y = y
		self.Theta1 = Theta1
		self.Theta2 = Theta2
		self.alive = True
		self.moves = 0
		self.game_matrix = game_matrix
		self.velocity = 0
		

	def move(self, x_goal, y_goal):

		if self.alive == True:
			x_change = 0
			y_change = 0

			inputs = self.look(x_goal, y_goal)

			action = self.think(inputs.ravel())
			
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
	def look(self, x_goal, y_goal):

		#we will look in all directions in a clockwise manner

		#look up
		up         = self.lookInDirection(x_goal, y_goal ,y=-1, x=0) 
		
		#look up/right
		up_right   = self.lookInDirection(x_goal, y_goal ,y=-1, x=1)
		
		#look right
		right      = self.lookInDirection(x_goal, y_goal ,y=0, x=1)
		
		#look down/right
		down_right = self.lookInDirection(x_goal, y_goal ,y=1, x=1)
		
		#look down
		down       = self.lookInDirection(x_goal, y_goal ,y=1, x=0)
		
		#look down/left
		down_left  = self.lookInDirection(x_goal, y_goal ,y=1, x=-1)
		
		#look left
		left       = self.lookInDirection(x_goal, y_goal ,y=0, x=-1)
		
		#look up/lefts
		up_left    = self.lookInDirection(x_goal, y_goal ,y=-1, x=-1)
	
		return np.hstack((up,up_right,right, down_right, down, down_left, left, up_left))
	
	def lookInDirection(self, x_goal, y_goal , y, x):
		goal_found = 0
		obs_distance = 1
		wall_distance = 1 #starting with 1 as it is the max value it can take
						  #input to the neural net is 1/wall_distance

		curr_x, curr_y  = self.get_position()
		check_x, check_y = curr_x + x, curr_y + y #moving one step in the looking direction

		curr_pos_val = self.game_matrix[check_y, check_x]  #game matrix accepts (y,x)

		#keep looking until you find an wall in this direction
		while check_y>0 and check_y<display_height and check_x>0 and check_x<display_width:

			#since there are chances of goal being an extended rectangle like thing
			#hence we will use the game matrix to search for the goal, instead of x_goal, y_goal
			
			curr_pos_val = self.game_matrix[check_y, check_x]    #game matrix accepts (y,x)
			
			if goal_found ==0  and curr_pos_val == 2:   #since the goal was marked with 2 in the game matrix
				goal_found = 1
			
			#break out of the loop if you find an obstacle in the path
			if curr_pos_val == -1:  #since the obstacle was marked with -1 in the game matrix
				obs_distance = wall_distance #as it was incremented at each step
				break
			
			wall_distance += 1

			#looking at the next block
			check_x += x
			check_y += y

		return np.array([1/wall_distance, 1/obs_distance,goal_found])

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
		
		#no descrimination on death type as of now
		self.alive = False
		return fitness

	def cal_fitness(self, x , y):
		distance = (x - x_goal)**2 + (y - y_goal)**2
		fitness = 10000/int(distance)
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

