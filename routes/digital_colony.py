import json
import logging
import json
from flask import jsonify

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def calculate_signature(a, b):
    diff = abs(a - b)
    if a > b:
        return diff
    elif a < b:
        return 10 - diff
    else:
        return 0

def next_generation(colony):
    weight = sum(int(digit) for digit in colony)
    new_colony = []
    
    for i in range(len(colony) - 1):
        a = int(colony[i])
        b = int(colony[i + 1])
        signature = calculate_signature(a, b)
        new_digit = (weight + signature) % 10
        new_colony.append(colony[i])
        new_colony.append(str(new_digit))
    
    new_colony.append(colony[-1])  # Add the last digit of the colony
    return ''.join(new_colony)

def calculate_weight_after_generations(colony, generations):
    for _ in range(generations):
        colony = next_generation(colony)
    return str(sum(int(digit) for digit in colony))

@app.route('/digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("Data sent for evaluation: {}".format(data))
    
    # Prepare the response array
    result = []
    
    for item in data:
        generations = item.get("generations")
        colony = item.get("colony")
        
        if generations is None or colony is None:
            logging.error("Invalid input: {}".format(item))
            return json.dumps({"error": "Invalid input"}), 400
        
        logging.info(f"Processing colony: {colony} for {generations} generations")
        final_weight = calculate_weight_after_generations(colony, generations)
        result.append(final_weight)
        logging.info(f"Final weight after {generations} generations: {final_weight}")
    
    logging.info("My result: {}".format(result))
    return json.dumps(result)