from maze_constants import EMPTY

def heuristic(a, b):
    """Manhattan distance heuristic for A* and Greedy BFS."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def depth_first_search(maze, start, goal):
    """Depth First Search algorithm for maze solving."""
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
    print(f"DFS visited {len(visited)} nodes and count is {count}")
    
    return path, visited

def breadth_first_search(maze, start, goal):
    """Breadth First Search algorithm for maze solving."""
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
    print(f"BFS visited {len(visited)} nodes and count is {count}")

    return path, visited

def a_star_search(maze, start, goal):
    """A* Search algorithm for maze solving."""
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
    print(f"A* visited {len(closed_set)} nodes and count is {count}")

    return path, closed_set

def greedy_best_first_search(maze, start, goal):
    """Greedy Best-First Search algorithm for maze solving."""
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
    print(f"Greedy BFS visited {len(closed_set)} nodes and count is {count}")

    return path, closed_set

# Placeholder functions for future implementation
def depth_limited_search(maze, current, goal, limit, visited, parent):
    """Depth Limited Search (to be implemented)."""
    return False

def iterative_deepening_search(maze, start, goal):
    """Iterative Deepening Search (to be implemented)."""
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
    print(f"IDS visited {len(visited)} nodes and count is {count}")

    return path, visited