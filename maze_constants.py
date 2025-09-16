import random
WIDTH = 21 # Width of the maze (must be odd).
HEIGHT = 15  # Height of the maze (must be odd).
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3
SEED = random.randint(1, 1000) # Change this number to get a different maze.
random.seed(SEED)

# Use these characters for displaying the maze:
EMPTY = '  '
MARK = '##'
WALL = chr(9608)+ chr(9608) # Character 9608 is '█'
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

RED = '\033[91m'
RESET = '\033[0m'
