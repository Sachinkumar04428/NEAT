#very easy game
import pygame
import random
from population import Population
import constants
import numpy as np 

pygame.init()

display_width = constants.display_width
display_height = constants.display_height

#colours
white= constants.white
black = constants.black
red = constants.red
blue = constants.blue
green = constants.green

#starting the display
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Easy game')

#clock
clock = pygame.time.Clock()

#goal
x_goal = constants.x_goal
y_goal = constants.y_goal

#obstacles
X_obs = constants.X_obstacles
Y_obs = constants.Y_obstacles

def draw_goal():
	pygame.draw.rect(gameDisplay, green, [x_goal,y_goal,constants.goal_width, constants.goal_height])

def display_obstacles():
	for x,y in zip(X_obs,Y_obs):
		pygame.draw.rect(gameDisplay, blue, [x,y, constants.obs_width, constants.obs_height])

def update_gen(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("gen: "+str(count), True, blue)
	#displaying the textBox
	gameDisplay.blit(text,(1,1))

def build_game_matrix():
	g_matrix = np.zeros(( display_height,display_width))
	
	#adding the boundaries
	pad = constants.padding_width
	g_matrix[0:pad,:] = 1
	g_matrix[display_height-pad:,:] = 1
	g_matrix[:,0:pad] = 1
	g_matrix[:,display_width-pad:] = 1

	#adding the goal
	g_matrix[ y_goal:y_goal+ constants.goal_height,
				x_goal:x_goal+constants.goal_width] = 2
	
	#adding obstacles
	g_matrix = add_obstacles(g_matrix)

	return g_matrix

def add_obstacles(g_matrix):
	for x, y in zip(X_obs, Y_obs):
		g_matrix[ y : y + constants.obs_height, x : x + constants.obs_width] = -1
	return g_matrix

def game_loop():
	
	game_matrix = build_game_matrix()
	pop = Population(constants.pop_size ,game_matrix)
	
	for gen in range(constants.max_generation):
		
		pop.increase_gen()
		game_over = False

		while not game_over:

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			pop.move(x_goal, y_goal)
			
			#checking if game_over
			game_over, won = pop.check_status()
			
			if won:
				print('Game Won')
				break
		
			#drawing to the screen
			gameDisplay.fill(black)
			display_obstacles()
			update_gen(gen)
			
			#dray goal
			draw_goal()

			#drawing the dots
			pop.draw(gameDisplay)
			
			pygame.display.update()
			clock.tick(60)  #60 frames per second

		if won:
			break

game_loop()
