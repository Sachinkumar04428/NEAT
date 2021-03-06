#population
import numpy as np
import random
from snake import Snake
from scipy import stats
import constants
import pandas as pd
import os
import time

save_at = 10

#constants
display_width = constants.display_width
display_height = constants.display_height

#snake
head_width = constants.head_width
head_height = constants.head_height

#food
food_width = constants.food_width
food_height = constants.food_height

#starting position
x_snake_start = constants.x_snake_start
y_snake_start = constants.y_snake_start

#hyperparameters 
MUTATION_PERCENT = constants.mutation_percent
#MAX_MOVES = constants.max_moves

#Neural Network hyperparameters
input_units = constants.input_units
hidden_units = constants.hidden_units
output_units = constants.output_units #up,right,left,down


class Population:

	def __init__(self,number):
		
		if number%2!=0:
			print('Please provide even number')
			raise Exception
		self.number = number  #number of individulals in a population
		self.gen = 0		  #initialised as generation 0
		self.fitness = [0 for i in range(self.number)] #inittialising all fitness to zero	  
		#Each snake in the population has a brain consisting of two matrices
		self.Theta1 = []    #stores the first weight matrix of every snake in pop
		self.Theta2 = []   	#stores the second weight matrix of each snake in population
		self.dead_count = 0    #setting all to alive
		self.pop = self.new_pop()  #list of individulas

	def new_pop(self):
		pop = []
		pad = constants.pad
		Theta1, Theta2 = self.get_weights(self.gen, self.Theta1, self.Theta2)
		for i in range(self.number):
			
			#x = int(random.randrange(pad,display_height-pad,step = head_width))
			#y = int(random.randrange(pad,display_width-pad,step=head_height))
			x, y = x_snake_start, y_snake_start
			snake = Snake(x, y, Theta1[i], Theta2[i])
			pop.append(snake)

		self.Theta1 , self.Theta2 = Theta1, Theta2
		return pop

	def increase_gen(self):
		self.gen += 1
		self.pop = self.new_pop()  #new population
		self.fitness = [0 for i in range(self.number)] #initialising all fitness to zero
		self.dead_count = 0    #setting all to alive

	def check_status(self, x_food, y_food):

		game_Over, ate_food = False, False
		pad_bound = 0
		for i,snake in enumerate(self.pop):

			if snake.is_Alive():
				x, y = snake.head_pos()
				
				if x<=pad_bound or x>=display_width-pad_bound or y<=pad_bound or y>=display_height-pad_bound:  #touching the boundaries
					self.kill_snake(i, snake)
				elif snake.bit_itself():
					self.kill_snake(i, snake)
				elif snake.get_moves() > snake.get_max_moves(self.gen):
					self.kill_snake(i, snake)

				#all snake are dead
				if self.all_dead():
					game_Over = True
					break
				
				#snake reaches the food
				if self.collided(x, y, head_width, head_height, x_food, y_food, food_width, food_height):
					snake.eat_food(x_food, y_food)
					ate_food = True
					
		return game_Over, ate_food

	def collided(self, x, y,width, height,  x_obs, y_obs, obs_width , obs_height):
		# A master function to detect snake collision between any two rectanges
		x_prime_1, x_prime_2 = x, x + width
		y_prime_1, y_prime_2 = y, y + height
		
		X_1, X_2 = x_obs, x_obs + obs_width
		Y_1, Y_2 = y_obs, y_obs + obs_height 

		if (x_prime_2 <= X_2 and x_prime_1 >= X_1) and (y_prime_2 <= Y_2 and y_prime_1 >= Y_1):
			return True
		return False

	def kill_snake(self, i, snake):
		self.fitness[i] = snake.kill(self.gen)
		self.dead_count += 1
	
	def all_dead(self):
		if self.dead_count==self.number:
			return True
		else:
			return False

	def draw(self, gameDisplay):
		for snake in self.pop:
			snake.draw(gameDisplay)

	def move(self,x_food, y_food):
		for snake in self.pop:
			snake.move(x_food, y_food)


	#Creating new weights using previous weights (different weights == different individuals)
	def get_weights(self,gen,Theta1,Theta2):
		
		global save_at

		if gen==0:	
			Theta1 = []
			Theta2 = []
			for i in range(self.number):
				Theta1.append(np.random.randn(hidden_units,input_units+1))
				Theta2.append(np.random.randn(output_units,hidden_units+1))
		else:
			Theta1,Theta2 = self.cross_breed(Theta1, Theta2, self.gen)

		if gen == save_at:
			save(gen,Theta1,Theta2)
			save_at += save_at
		return Theta1, Theta2
		
	#cross breeding previous gen to make new ones
	def cross_breed(self, Theta1, Theta2, gen):
		
		fitness = np.array(self.fitness)
		print('max fitness',np.max(fitness))
		sum_ = np.sum(fitness)

		#multiplying by 500, so as to keep the size of mating pool to be around 500
		fitness = np.around((fitness*2000)/sum_)

		#saving the best for later use
		best_index = np.argmax(fitness)
		save_best(gen,Theta1[best_index],Theta2[best_index])

		#creating the mating pool
		mating_pool = []
		for i in range(fitness.shape[0]): 
			n = int(fitness[i])
			for j in range(n):
				mating_pool.append(i)
		
		size = len(mating_pool)
		mating_pool = np.array(mating_pool)

		#checking if the one with highest fitness
		#Is the one with max copies in mating pool
		print('snake with highest fitness:',np.argmax(fitness))
		print('snake with highest occurence in mating pool:',stats.mode(mating_pool)[0], end='\n\n')

		Theta1_new = [0 for i in range(self.number)]
		Theta2_new = [0 for i in range(self.number)]

		for i in range(0,self.number,2):
			#selecting two random individuals from mating pool
			rand_index_1 = random.randint(0,size-1)
			rand_index_2 = random.randint(0,size-1)
			parent_1 = mating_pool[rand_index_1]
			parent_2 = mating_pool[rand_index_2]

			fit_1 = len(np.where(mating_pool==parent_1)[0])
			fit_2 = len(np.where(mating_pool==parent_2)[0])
			
			#creating two new individuals from the above selected individuals
			Theta1_new[i], Theta1_new[i+1] = mate(Theta1[parent_1], Theta1[parent_2], fit_1, fit_2)  
			Theta2_new[i], Theta2_new[i+1] = mate(Theta2[parent_1], Theta2[parent_2], fit_1, fit_2)
			
		return Theta1_new, Theta2_new

def mate(theta1, theta2, fit_1, fit_2):
	shape = theta1.shape
	#flattening the matrices
	theta1, theta2 = theta1.ravel(), theta2.ravel()
	size = theta1.shape[0]

	#number of genes to be selected from parent 1 
	#parent 2 would be then size-gene_1
	gene_1 = int((fit_1*size) / (fit_1 + fit_2))
	
	#dividing chromosom size into 2 group of RANDOM GENE LOCATIONS 
	# of sizes proportional to number of genes to be selected from each parent 
	random_array = np.random.permutation(np.arange(size))
	rand_indices_1 = random_array[:gene_1]
	rand_indices_2 = random_array[gene_1:]

	#creating two new chromosomes
	theta1_new = np.zeros(size)
	theta2_new = np.zeros(size)

	#passing genes of selected GENE LOCATIONS from both the parents
	theta1_new[rand_indices_1] = theta1[rand_indices_1]  # from parent 1
	theta1_new[rand_indices_2] = theta2[rand_indices_2]  # from parent 2

	theta2_new[rand_indices_1] = theta2[rand_indices_1]  #from parent 2
	theta2_new[rand_indices_2] = theta1[rand_indices_2]  #from parent 1
	
	#mutating the new childs  (hell yeah!)
	theta1_new = mutate(theta1_new)
	theta2_new = mutate(theta2_new)
	
	#converting vectors to matrices
	theta1_new , theta2_new = theta1_new.reshape(shape), theta2_new.reshape(shape)
	return theta1_new, theta2_new

def mutate(theta1):
	if(random.randint(0,99)<MUTATION_PERCENT):
		#selecting  a random index/gene to mutate
		rand_index = random.randint(0,theta1.shape[0]-1)
		#setting the random gene to a random number 
		theta1[rand_index] = random.randint(0,1)*np.mean(theta1)

	return theta1

def save(gen, Theta1, Theta2):

	Th_1 = np.hstack([theta.ravel() for theta in Theta1])
	Th_2 = np.hstack([theta.ravel() for theta in Theta2])
	
	#making pandas Series
	theta1_df = pd.Series(Th_1)
	theta2_df = pd.Series(Th_2)

	folder_name = f'training 6/gen{gen}'
	try:
		os.mkdir(folder_name)
	except FileExistsError:
		pass
	#saving it
	theta1_name = f'theta1_gen{gen}'
	theta2_name = f'theta2_gen{gen}'

	theta1_df.to_csv(f'{folder_name}/{theta1_name}.csv')
	theta2_df.to_csv(f'{folder_name}/{theta2_name}.csv')
	print(f'gen{gen} weights saved')

def save_best(gen,theta1, theta2):

	folder_name = f'training 6/gen{gen}'

	try:
		os.mkdir(folder_name)
	except FileExistsError:
		pass
	
	theta1_df = pd.DataFrame(theta1)
	theta2_df = pd.DataFrame(theta2)

	theta1_df.to_csv(f'{folder_name}/theta1_best.csv')
	theta2_df.to_csv(f'{folder_name}/theta2_best.csv')
