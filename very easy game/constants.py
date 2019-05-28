
display_width = 300
display_height = 300

#colours
white= (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,245,0)

#dot 
x_dot_start = int(display_width/2)
y_dot_start = 50
dot_width = 3
dot_height = 3

#obstacle
X_obstacles = [0, 150]
Y_obstacles = [150, 200]
obs_width = 150
obs_height = 4

#goal line
x_goal = 150
y_goal = 275
goal_width = 4 
goal_height = 4

#model hyperparameters
max_moves = 500
mutation_percent = 2
pop_size = 500
max_generation = 100

#vision parameters
forward_vision = 6
#side vision is f_vision/2
padding_width = forward_vision

#Neural net parameteres
input_units = 6*6 + 2
hidden_units = 100
output_units = 4

