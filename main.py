"""
Maze Solver - Main Program
Ahmed Hussein 2025
Based on maze generation algorithm from Al Sweigart
"""

import sys
import time
from maze_generation import generate_maze, print_maze
from maze_search_algorithms import depth_first_search, breadth_first_search, a_star_search, greedy_best_first_search
from maze_constants import WIDTH, HEIGHT, SEED, MARK

def print_path_on_maze(maze, path):
    """Print the maze with the solution path marked."""
    maze_with_path = maze.copy()
    for (x, y) in path:
        maze_with_path[(x, y)] = MARK
    print_maze(maze_with_path)

def print_visited_on_maze(maze, visited):
    """Print the maze with visited nodes marked."""
    maze_with_visited = maze.copy()
    for (x, y) in visited:
        maze_with_visited[(x, y)] = '()'
    print_maze(maze_with_visited)

def main():
    """Main function to generate and solve a maze."""
    # Generate the maze
    print(f"Generating maze with SEED {SEED}...")
    maze = generate_maze()
    print("Maze has volume of", WIDTH * HEIGHT, "units.")
    print_maze(maze)
    
    # Define start and goal positions
    start = (1, 1)
    goal = (WIDTH - 2, HEIGHT - 2)
    
    # Solve using different algorithms
    print("\n=== A* Search ===")
    path, visited = a_star_search(maze, start, goal)
    print_path_on_maze(maze, path)
    
    print("\n=== Depth First Search ===")
    path, visited = depth_first_search(maze, start, goal)
    print_path_on_maze(maze, path)
    
    print("\n=== Breadth First Search ===")
    path, visited = breadth_first_search(maze, start, goal)
    print_path_on_maze(maze, path)
    
    print("\n=== Greedy Best-First Search ===")
    path, visited = greedy_best_first_search(maze, start, goal)
    print_path_on_maze(maze, path)

if __name__ == "__main__":
    main()