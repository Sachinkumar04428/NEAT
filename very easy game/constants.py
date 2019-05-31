
display_width = 200
display_height = 200

#colours
white= (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,245,0)

#dot 
x_dot_start = int(display_width/2)
y_dot_start = 20
dot_width = 3
dot_height = 3

#obstacle
X_obstacles = [75]
Y_obstacles = [100]
obs_width = 50
obs_height = 4

#goal line
x_goal = 100
y_goal = 175
goal_width = 4 
goal_height = 4

#model hyperparameters
max_moves = 550
mutation_percent = 15
pop_size = 50
max_generation = 100

#the number of pixels around the boundary to be
#marked as obstacle
padding_width = 4

#Neural net parameteres
input_units = 24
hidden_units = 16
output_units = 4

