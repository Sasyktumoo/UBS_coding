import json
import logging
from flask import jsonify, request
from routes import app

logger = logging.getLogger(__name__)

MOVE_MAP = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1)
}

def string_to_grid(board_str):
    return [list(board_str[i:i + 4]) for i in range(0, 20, 4)]

def grid_to_string(grid):
    return ''.join(''.join(row) for row in grid)

def get_block_locations(board):
    blocks = {}
    checked = [[False for _ in range(4)] for _ in range(5)]
    
    for i in range(5):
        for j in range(4):
            block = board[i][j]
            if block != '@' and not checked[i][j]:
                positions = []
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if checked[x][y]:
                        continue
                    checked[x][y] = True
                    positions.append((x, y))
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 5 and 0 <= ny < 4 and board[nx][ny] == block and not checked[nx][ny]:
                            stack.append((nx, ny))
                
                blocks[block] = positions
    return blocks

def do_move(board, blocks, block, move):
    di, dj = MOVE_MAP[move]
    
    current_positions = blocks[block]
    new_positions = []
    
    for (i, j) in current_positions:
        ni, nj = i + di, j + dj
        if not (0 <= ni < 5 and 0 <= nj < 4):
            return board, blocks
        if board[ni][nj] != '@' and (ni, nj) not in current_positions:
            return board, blocks
        new_positions.append((ni, nj))
    
    for i, j in current_positions:
        board[i][j] = '@'
    
    for i, j in new_positions:
        board[i][j] = block
    
    blocks[block] = new_positions
    
    return board, blocks

def run_klotski(board_str, moves_str):
    board = string_to_grid(board_str)
    blocks = get_block_locations(board)
    
    for i in range(0, len(moves_str), 2):
        block = moves_str[i]
        move = moves_str[i + 1]
        board, blocks = do_move(board, blocks, block, move)
    
    return grid_to_string(board)

@app.route('/klotski', methods=['POST'])
def klotski_handler():
    data = request.get_json()
    final_boards = []
    
    for game in data:
        board_str = game.get("board", [])
        moves_str = game.get("moves", [])
        final_board = run_klotski(board_str, moves_str)
        final_boards.append(final_board)
    
    return jsonify(final_boards)

