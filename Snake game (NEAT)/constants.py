#colours
white= (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,245,0)
orange = (255,165,0)

#snake 
head_width = 10
head_height = 10

#food
food_width = 10
food_height = 10
food_padding = food_width*2

#model hyperparameters
mutation_percent = 10
pop_size = 400
max_generation = 500

#Neural net parameteres
input_units = 24 
hidden_units = 18
output_units = 4

pad = food_padding

#display screen
display_width = head_width*40
display_height = head_height*40


#position of starting of snake
x_snake_start = int(display_width/2)
y_snake_start = int(display_height/2)