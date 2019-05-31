import pygame
import math
import random
from snake import Snake
import time

pygame.init()

#Constants
display_width = 600
display_height = 600

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
score_color = (0,0,220)

#starting points
x_start = display_width/2
y_start = display_height/2

#snake parts
snake_width = 10
snake_height = 10

#food
food_width = 10
food_height = 10

#rendering the screen
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
game_over = False


#critical collision distance
crit_x = (food_width + snake_width)/2
crit_y = (food_height + snake_height)/2

def collision():
	message_display("You Lost")

def bitten():
	message_display("you bit yourself!")

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf', 100)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)
	pygame.display.update()  #don't forget to update this! NEVER///
	time.sleep(2)
	game_loop()

def text_objects(text, font):
	textSurface = font.render(text, True, white)
	return textSurface, textSurface.get_rect()


def draw_food(x,y):
	pygame.draw.rect(gameDisplay, green, [x,y,food_width,food_height])

def score_update(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("Score: "+str(count), True, score_color)
	gameDisplay.blit(text,(1,1))		

def game_loop():

	#starting position
	snake = Snake(snake_width,snake_height, x_start, y_start)
	
	x_food = random.randrange(0,display_width-food_width,food_width)
	y_food = random.randrange(0,display_height-food_height,food_height)
	score = 0

	while not game_over:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			snake.move(event)

		#draw things
		bite = snake.update_position()

		gameDisplay.fill(black)
		snake.draw(gameDisplay)
		draw_food(x_food,y_food)
		score_update(score)
		
		x_head, y_head = snake.head()
		
		#collision detection
		if abs(x_head-x_food) < crit_x and abs(y_head - y_food) < crit_y:
			snake.eat_food()
			score +=1
			x_food = random.randrange(0,display_width-food_width,food_width)  #Since it includes the end point also
			y_food = random.randrange(0,display_height-food_height,food_height) 

		
		if x_head <0 or x_head > display_width or y_head<0 or y_head>display_height:
			snake.kill()
			collision()

		if bite:
			bitten()

		#always remember to update the display
		pygame.display.update()
		clock.tick(20)

game_loop()
pygame.quit()
quit()