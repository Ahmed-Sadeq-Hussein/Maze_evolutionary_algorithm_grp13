import random
import sys
import time
import pygame
## Ahmed Hussein 2025
## Imported Maze Solution from Al Sweigart https://inventwithpython.com/recursion/chapter11.html
## Edited slightly to fit the lesson plan and easier visuals .
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

# Create the filled-in maze data structure to start:
maze = {}
for x in range(WIDTH):
    for y in range(HEIGHT):
        maze[(x, y)] = WALL # Every space is a wall at first.

def printMaze(maze, markX=None, markY=None):
    """Displays the maze data structure in the maze argument. The
    markX and markY arguments are coordinates of the current
    '@' location of the algorithm as it generates the maze."""

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if markX == x and markY == y:
                # Display the '@' mark here:
                print(MARK, end='')
            if maze[(x, y)] != WALL:
                ##Prints tokens in red 
                print('\033[91m' + maze[(x, y)] + '\033[0m', end='')
                # Display the empty space:
                
            else:
                # Display the wall or empty space:
                print(maze[(x, y)], end='')
        print() # Print a newline after printing the row.


def visit(x, y):
    """Carve out empty spaces in the maze at x,y. In addition to the normal
    recursive backtracker carving, occasionally create a long-range 'bridge'
    to a previously visited intersection to produce alternative paths
    (shortcuts) between different branches of the maze."""
    maze[(x, y)] = EMPTY  # carve current

    while True:
        # find unvisited neighbors two steps away (intersections)
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)
        if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)
        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)
        if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        if len(unvisitedNeighbors) == 0:
            # dead end -> backtrack
            return
        else:
            # standard step to a random unvisited neighbor
            nextIntersection = random.choice(unvisitedNeighbors)

            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = EMPTY  # connecting hallway
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = EMPTY
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = EMPTY
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = EMPTY

            hasVisited.append((nextX, nextY))
            visit(nextX, nextY)

            # ---------------------------
            # Occasionally create a long-range shortcut ("bridge")
            # ---------------------------
            bolcondition = False # Change to false to disable bridges
            
            BRIDGE_PROB = 0.05     # tweak up/down to get more/fewer shortcuts
            MIN_DISTANCE = 3       # only connect to visited intersections at least this far away
            if random.random() < BRIDGE_PROB and len(hasVisited) > 6:
                # choose candidate visited intersections far enough away
                candidates = [v for v in hasVisited
                              if v != (x, y) and abs(v[0] - x) + abs(v[1] - y) >= MIN_DISTANCE]
                if candidates:
                    # weight candidates towards the bottom-right goal to increase chance of start<->goal shortcuts
                    goal_coord = (WIDTH - 2, HEIGHT - 2)
                    weights = []
                    for v in candidates:
                        d_goal = abs(v[0] - goal_coord[0]) + abs(v[1] - goal_coord[1])
                        # smaller distance to goal -> larger weight
                        weights.append(1.0 / (d_goal + 1))

                    target = random.choices(candidates, weights=weights, k=1)[0]

                    # carve an L-shaped corridor from (x,y) to target (step 1 cell at a time)
                    cx, cy = x, y
                    while (cx, cy) != target:
                        if cx != target[0]:
                            cx += 1 if target[0] > cx else -1
                        elif cy != target[1]:
                            cy += 1 if target[1] > cy else -1
                        maze[(cx, cy)] = EMPTY
                        # if we carved an intersection (odd,odd), mark it visited so the generator won't treat it as unvisited later
                        if cx % 2 == 1 and cy % 2 == 1 and (cx, cy) not in hasVisited:
                            hasVisited.append((cx, cy))





##############################################################################################################################
## Adding a visited set to return the path taken by the algorithm
def depth_first_search(maze, start, goal):
    stack = [start]
    count = 0
    visited = set()
    parent = {start: None}

    while stack:
        count += 1
        current = stack.pop()
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if maze.get(neighbor) == EMPTY and neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current

    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    print(f"DFS visited {len(visited)} nodes and count is " + count.__str__())
    
    return path , visited
##############################################################################################################################
def breath_first_search(maze, start, goal):
    queue = [start]
    visited = set()
    parent = {start: None}
    count = 0
    while queue:
        count += 1
        current = queue.pop(0)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if maze.get(neighbor) == EMPTY and neighbor not in visited:
                queue.append(neighbor)
                parent[neighbor] = current
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    print(f"BFS visited {len(visited)} nodes and count is " + count.__str__())

    return path, visited

##############################################################################################################################
## A* search algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(maze, start, goal):
    open_set = {start}
    closed_set = set()
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    parent = {start: None}
    count = 0

    while open_set:
        count += 1
        current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
        if current == goal:
            break

        open_set.remove(current)
        closed_set.add(current)

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if maze.get(neighbor) != EMPTY or neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            parent[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    print(f"A* visited {len(closed_set)} nodes and count is " + count.__str__())

    return path, closed_set

##############################################################################################################################
##greedy first search
def greedy_best_first_search(maze, start, goal):
    open_set = {start}
    closed_set = set()
    parent = {start: None}
    count = 0

    while open_set:
        count += 1
        current = min(open_set, key=lambda pos: heuristic(pos, goal))
        if current == goal:
            break

        open_set.remove(current)
        closed_set.add(current)

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if maze.get(neighbor) != EMPTY or neighbor in closed_set:
                continue

            if neighbor not in open_set:
                open_set.add(neighbor)
                parent[neighbor] = current

    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    print(f"Greedy BFS visited {len(closed_set)} nodes and count is " + count.__str__())

    return path, closed_set
##############################################################################################################################
## Depth limited first search /Not completed
def depth_limited_search(maze, current, goal, limit, visited, parent):
    return False


##############################################################################################################################
##  iterative deepening search 
def iterative_deepening_search(maze, start, goal):
    depth = 0
    visited = set()
    parent = {start: None}
    count = 0

    while True:
        count += 1
        visited.clear()
        parent.clear()
        parent[start] = None
        if depth_limited_search(maze, start, goal, depth, visited, parent):
            break
        depth += 1

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    print(f"IDS visited {len(visited)} nodes and count is " + count.__str__())

    return path, visited
##############################################################################################################################
## EVOLUTIONARY PROGRAMMING!!!! 
## We want to evolve a population of mazes towards a goal of having a path from start to finish. .
## Each maze is represented as a 2D grid of cells, where each cell can be either a wall or an empty space.
## Modifiers we need to consider are how close we are to the goal, exploration vs exploitation,
## Fitness function, exit proximity reward, exploration reward , legal move reward, dead end penality.
## Add thinking and perception to better results .
## https://www.youtube.com/watch?v=XP2sFzp2Rig 



##############################################################################################################################
##Printing solutions 

def print_path_on_maze(maze, path):
    maze_with_path = maze.copy()
    for (x, y) in path:
        maze_with_path[(x, y)] = MARK
    printMaze(maze_with_path)

def print_visited_on_maze(maze, visited):
    maze_with_visited = maze.copy()
    for (x, y) in visited:
        maze_with_visited[(x, y)] = '()'
    printMaze(maze_with_visited)


##############################################################################################################################
##### Generate and display the maze:
# Carve out the paths in the maze data structure:
hasVisited = [(1, 1)] # Start by visiting the top-left corner.
visit(1,1)
goal = [(WIDTH - 2, HEIGHT - 2)]
printMaze(maze)

##### Main program logic:
##We will also print the walked paths of the algorithms to see how they traversed the maze
print(f"Generating maze with SEED {SEED}...")
print("Perspective the maze has volume of " + (WIDTH * HEIGHT).__str__() + " units.")
awnser, visited = a_star_search(maze, (1, 1), (WIDTH - 2, HEIGHT - 2))
print_path_on_maze(maze, awnser)
print_visited_on_maze(maze, visited)
#print_path_on_maze(maze, awnser)
# Display the final resulting maze data structure:

## We can try to display the puzzle through the window using pygame
## We print the path taken by the algorithm




