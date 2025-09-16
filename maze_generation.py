import random
from maze_constants import *

# Global variable for tracking visited cells during generation
hasVisited = []

def generate_maze():
    """Generate a maze using recursive backtracking algorithm."""
    global hasVisited
    
    # Create the filled-in maze data structure to start:
    maze = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            maze[(x, y)] = WALL  # Every space is a wall at first.

    # Initialize visited list
    hasVisited = [(1, 1)]  # Start by visiting the top-left corner.
    
    # Generate the maze
    visit(1, 1, maze)
    
    return maze

def visit(x, y, maze):
    """Carve out empty spaces in the maze at x,y using recursive backtracking."""
    global hasVisited
    
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
            visit(nextX, nextY, maze)

            # ---------------------------
            # Occasionally create a long-range shortcut ("bridge")
            # ---------------------------
            bridge_condition = True  # Change to true to enable bridges
            
            BRIDGE_PROB = 0.05     # tweak up/down to get more/fewer shortcuts
            MIN_DISTANCE = 3       # only connect to visited intersections at least this far away
            
            if bridge_condition and random.random() < BRIDGE_PROB and len(hasVisited) > 6:
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

def print_maze(maze, markX=None, markY=None):
    """Displays the maze data structure in the maze argument."""
   
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if markX == x and markY == y:
                # Display the '@' mark here:
                print(MARK, end='')
            elif maze[(x, y)] != WALL:
                # Prints tokens in red 
                print(RED + maze[(x, y)] + RESET, end='')
            else:
                # Display the wall or empty space:
                print(maze[(x, y)], end='')
        print()  # Print a newline after printing the row.