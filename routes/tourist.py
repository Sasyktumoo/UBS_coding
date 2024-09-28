import json
import logging
from flask import jsonify

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def find_best_path(locations, start, time_limit):
    # Backtracking helper function
    def backtrack(path, current_station, time_spent, satisfaction, best_result):
        # If time spent exceeds the time limit, prune
        if time_spent > time_limit:
            return
        
        # If we are back at the starting point after visiting other stations, check satisfaction
        if len(path) > 1 and current_station == start:
            if satisfaction > best_result['satisfaction']:
                best_result['path'] = path[:]
                best_result['satisfaction'] = satisfaction
            return

        # Explore other stations
        for next_station in locations:
            if next_station not in path or next_station == start:  # Can revisit start only
                next_satisfaction, next_time = locations[next_station]
                # Try this station if time permits, and it's not the same as the current station
                if current_station != next_station:
                    backtrack(path + [next_station], next_station, 
                              time_spent + next_time, satisfaction + next_satisfaction, best_result)

    # Best result initialization
    best_result = {'path': [], 'satisfaction': 0}

    # Start backtracking from the starting point
    backtrack([start], start, 0, 0, best_result)
    
    return best_result

@app.route('/tourist', methods=['POST'])
def tourist():
    # Parse the input JSON
    data = request.json
    locations = data['locations']
    starting_point = data['startingPoint']
    time_limit = data['timeLimit']
    
    # Solve the tourist problem
    result = find_best_path(locations, starting_point, time_limit)
    
    return jsonify(result)