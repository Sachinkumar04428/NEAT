import pygame
import math
import random
import time
from population import Population
from snake import Snake
import time
import constants

pygame.init()

display_width = constants.display_width
display_height = constants.display_height

#colours
white= constants.white
black = constants.black
red = constants.red
blue = constants.blue
green = constants.green
orange = constants.orange

#rendering the screen
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

#food
food_width = constants.food_width 
food_height = constants.food_height


def draw_food(x,y):
	pygame.draw.rect(gameDisplay, green, [x,y,food_width,food_height])

def update_gen(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("gen: "+str(count), True, orange)
	gameDisplay.blit(text,(5,5))

def game_loop():
	
	pop = Population(constants.pop_size)
	
	pad = constants.pad  #to avoid food getting to much at the boundaries
	
	#the first food
	x_food = random.randrange(pad,display_width-pad, step = food_width)
	y_food = random.randrange(pad,display_height-pad, step = food_height)
	print('food',x_food,y_food)
	score = 0
	food_not_eaten = 0
	
	for gen in range(constants.max_generation):
	
		game_over = False
		print('Generation',gen)

		while not game_over:

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			#moving the population
			pop.move(x_food, y_food)
			
			#checking if game_over
			game_over, ate_food = pop.check_status(x_food, y_food)

			#displaying it
			gameDisplay.fill(black)
			draw_food(x_food, y_food)
			update_gen(gen)
			pop.draw(gameDisplay)


			pygame.display.update()
			clock.tick(50)

			
			#updates
			if(ate_food):
				x_food = random.randrange(pad,display_width-pad, step = food_width)
				y_food = random.randrange(pad,display_height-pad, step = food_height)

			if(game_over):
				break	
		
		#changing food coordinates after each gen in the hope of getting better training results
		if not ate_food:
			x_food = random.randrange(pad,display_width-pad, step = food_width)
			y_food = random.randrange(pad,display_height-pad, step = food_height)
		
		pop.increase_gen()

		
game_loop()