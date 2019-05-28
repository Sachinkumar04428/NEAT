#population
import numpy as np
import random
from dot import Dot
from scipy import stats
import constants

#constants
display_width = constants.display_width
display_height = constants.display_height

dot_width = constants.dot_width
dot_height = constants.dot_height

#hyperparameters 
MUTATION_PERCENT = constants.mutation_percent
MAX_MOVES = constants.max_moves

#Neural Network hyperparameters
input_units = constants.input_units
hidden_units = constants.hidden_units
output_units = constants.output_units #up,right,left,down

#Obstacles
X_obs = constants.X_obstacles
Y_obs = constants.Y_obstacles
obs_width = constants.obs_width
obs_height = constants.obs_height

#pad 
pad = constants.padding_width

class Population:

	def __init__(self,number,game_matrix):
		
		if number%2!=0:
			print('Please provide even number')
			raise Exception
		self.number = number  #number of individulals in a population
		self.gen = 0		  #initialised as generation 0
		self.pop = []		  #list of individulas
		self.Theta1 = []
		self.Theta2 = []
		self.game_matrix = game_matrix
		print(game_matrix.shape,'is game matrix')

	def new_pop(self):
		pop = []
		Theta1, Theta2 = self.get_weights(self.gen, self.Theta1, self.Theta2)
		for i in range(self.number):
			x = constants.x_dot_start
			y = constants.y_dot_start
			
			dot = Dot(x,y, Theta1[i], Theta2[i], self.game_matrix)
			pop.append(dot)

		self.Theta1 , self.Theta2 = Theta1, Theta2
		return pop

	def increase_gen(self):
		self.gen += 1
		self.pop = self.new_pop()
		self.fitness = [0 for i in range(self.number)] #inittialising all fitness to zero
		self.dead_count = 0    #setting all to alive

	def check_status(self):

		game_Over = False
		won = False
		death_type = -1

		for i,dot in enumerate(self.pop):

			if dot.isAlive():
				x, y = dot.get_position()
				
				if x<=pad or x>=display_width-pad or y<=pad or y>=display_height-pad:  #outside the display area
					death_type = 1
					self.kill_dot(i, dot, death_type)
				
				for x_obs,y_obs in zip(X_obs, Y_obs):
					if self.collided(x, y, dot_width, dot_height, x_obs, y_obs, obs_width ,obs_height):
						death_type = 2
						self.kill_dot(i, dot, death_type)
				
				#moves over
				if dot.get_moves() >= MAX_MOVES and dot.isAlive():
					death_type = 3
					self.kill_dot(i, dot, death_type)
		
				#all dots are dead
				if self.all_dead():
					game_Over = True
					break
				
				#dot reaches the end
				if self.collided(x, y, dot_width, dot_height, constants.x_goal, constants.y_goal, constants.goal_width, constants.goal_height):
					print('AT',y)
					game_Over , won = True, True
					break

		return game_Over, won

	def collided(self, x, y,width, height,  x_obs, y_obs, obs_width , obs_height):
		# A master function to detect dot collision between any two rectanges
		x_prime_1, x_prime_2 = x, x + width
		y_prime_1, y_prime_2 = y, y + height
		
		X_1, X_2 = x_obs, x_obs + obs_width
		Y_1, Y_2 = y_obs, y_obs + obs_height 

		if (x_prime_1 <= X_2 and x_prime_2 >= X_1) and (y_prime_1 <= Y_2 and y_prime_2 >= Y_1):
			return True
		return False

	def kill_dot(self, i, dot, death_type):
		self.fitness[i] = dot.kill(death_type)
		self.dead_count += 1
	
	def all_dead(self):
		if self.dead_count==self.number:
			return True
		else:
			return False

	def draw(self, gameDisplay):
		for dots in self.pop:
			dots.draw(gameDisplay)

	def move(self):
		for dots in self.pop:
			dots.move()


	#Creating new weights using previous weights (different weights == different individuals)
	def get_weights(self,gen,Theta1,Theta2):
		
		if gen==1:	
			Theta1 = []
			Theta2 = []
			for i in range(self.number):
				Theta1.append(np.random.randn(hidden_units,input_units+1))
				Theta2.append(np.random.randn(output_units,hidden_units+1))
		else:
			Theta1,Theta2 = self.cross_breed(Theta1, Theta2, self.gen)

		return Theta1, Theta2

	#cross breeding previous gen to make new ones
	def cross_breed(self, Theta1, Theta2, gen):
		
		fitness = np.array(self.fitness)
		print('max fitness ',np.max(fitness))
		sum = int(np.sum(fitness))
		fitness = (fitness/sum)*4000*(gen)
		'''
			Since with increasing performance  and gen, sum increases
			and thus average fitness decreases, so multiplying with gen**2
			to maintain the number of different individuals
		'''
		print('max fitness after normalization',np.max(fitness))
		
		mating_pool = []
		for i in range(fitness.shape[0]): 
			n = int(fitness[i])
			for j in range(n):
				mating_pool.append(i)
		
		size = len(mating_pool)
		
		#checking if the one with highest fitness
		#Is the one with highest chance of mating
		print('do this match',np.argmax(fitness),stats.mode(mating_pool)[0])

		Theta1_new = [0 for i in range(self.number)]
		Theta2_new = [0 for i in range(self.number)]

		for i in range(0,self.number,2):
			#selecting two random individuals from mating pool
			a = mating_pool[random.randint(0,size-1)]
			b = mating_pool[random.randint(0,size-1)]

			#creating two new individuals from the above selected individuals
			Theta1_new[i], Theta1_new[i+1] = mate(Theta1[a], Theta1[b])  
			Theta2_new[i], Theta2_new[i+1] = mate(Theta2[a], Theta2[b])
			
		return Theta1_new, Theta2_new

def mate(theta1, theta2):
	shape = theta1.shape
	theta1, theta2 = theta1.ravel(), theta2.ravel()
	#selecting the cross over point to be half
	cross_over_point = int(theta1.shape[0]/2)

	theta1_new = np.hstack((theta1[:cross_over_point],theta2[cross_over_point:]))
	theta2_new = np.hstack((theta1[cross_over_point:],theta2[:cross_over_point]))

	theta1_new = mutate(theta1_new)
	theta2_new = mutate(theta2_new)
	
	theta1_new , theta2_new = theta1_new.reshape(shape), theta2_new.reshape(shape)
	return theta1_new, theta2_new

def mutate(theta1):
	if(random.randint(0,99)<MUTATION_PERCENT):
		#selecting  a random index/gene to mutate
		rand_index = random.randint(0,theta1.shape[0]-1)
		#setting the random gene to a random number 
		theta1[rand_index] = random.randint(0,1)*np.mean(theta1)

	return theta1

