from maze_constants import *
from maze_generation import generate_maze, print_maze

if __name__ == '__main__':
    maze = generate_maze()
    print(f'Seed: {SEED}')
    print_maze(maze)