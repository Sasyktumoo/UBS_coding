import json
import logging
from copy import deepcopy
from collections import deque
from flask import jsonify

from flask import request

from routes import app

logger = logging.getLogger(__name__)

MOVES = {
    'u': (-1, 0),  # Move up
    'd': (1, 0),   # Move down
    'l': (0, -1),  # Move left
    'r': (0, 1)    # Move right
}

# Bullet movement directions
BULLET_MOVES = {
    'u': (-1, 0),  # Bullet moves up
    'd': (1, 0),   # Bullet moves down
    'l': (0, -1),  # Bullet moves left
    'r': (0, 1)    # Bullet moves right
}

def in_bounds(x, y, grid):
    """Check if (x, y) is within the bounds of the grid."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def move_bullets(grid):
    """Simulate bullet movement on the grid."""
    new_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in BULLET_MOVES:
                dx, dy = BULLET_MOVES[grid[i][j]]
                new_x, new_y = i + dx, j + dy
                if in_bounds(new_x, new_y, grid):
                    # Move bullet to the new position, bullets can overlap
                    new_grid[new_x][new_y] = grid[i][j]
    
    return new_grid

def is_safe(x, y, grid):
    """Check if the position (x, y) is safe (not hit by a bullet)."""
    return in_bounds(x, y, grid) and grid[x][y] == '.'

def find_player_position(grid):
    """Find the player's position (*) on the grid."""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '*':
                return i, j
    return None

def dodge_bullets(grid, max_steps=10):
    """Find the safest sequence of moves to dodge bullets."""
    player_x, player_y = find_player_position(grid)
    
    # We will use BFS to explore possible moves and track the paths
    queue = deque([((player_x, player_y), [], grid)])  # ((x, y), path, current grid state)
    visited = set([(player_x, player_y, str(grid))])  # Keep track of visited positions and grid states
    
    while queue:
        (x, y), path, current_grid = queue.popleft()
        
        # If path length exceeds max_steps, we stop
        if len(path) >= max_steps:
            continue
        
        # Simulate bullet movement after the player moves
        next_grid = move_bullets(current_grid)
        
        # Try all possible moves (up, down, left, right)
        for move, (dx, dy) in MOVES.items():
            new_x, new_y = x + dx, y + dy
            
            # Check if the new position is safe
            if is_safe(new_x, new_y, next_grid) and (new_x, new_y, str(next_grid)) not in visited:
                new_path = path + [move]
                visited.add((new_x, new_y, str(next_grid)))
                
                # If we find a valid path, return it
                return new_path
                
                # Continue exploring all safe paths
                queue.append(((new_x, new_y), new_path, next_grid))
    
    # If no safe moves found, return None
    return None

@app.route('/dodge', methods=['POST'])
def dodge():
    data = request.json
    grid = data['map']
    
    # Find the best sequence of moves to dodge bullets
    instructions = dodge_bullets(grid)
    
    # If no valid path is found, return {"instructions": null}
    if instructions is None:
        return jsonify({"instructions": None})
    else:
        return jsonify({"instructions": instructions})