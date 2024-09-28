import json
import logging
from flask import Flask, request

app = Flask(__name__)
logger = logging.getLogger(__name__)

def calculate_weight(colony):
    return sum(int(digit) for digit in colony)

def calculate_signature(a, b):
    if a >= b:
        return a - b
    else:
        return 10 - (b - a)

def next_generation(colony):
    weight = calculate_weight(colony)
    new_colony = []
    for i in range(len(colony) - 1):
        a, b = int(colony[i]), int(colony[i + 1])
        signature = calculate_signature(a, b)
        new_digit = (weight + signature) % 10
        new_colony.append(colony[i])
        new_colony.append(str(new_digit))
    new_colony.append(colony[-1])
    return "".join(new_colony)

def calculate_final_weight(initial_colony, generations):
    colony = initial_colony
    for _ in range(generations):
        colony = next_generation(colony)
    return str(calculate_weight(colony))

@app.route('/digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("Data sent for evaluation: {}".format(data))

    results = []
    for item in data:
        generations = item['generations']
        colony = item['colony']
        weight = calculate_final_weight(colony, generations)
        results.append(weight)

    logging.info("Results: {}".format(results))
    return json.dumps(results)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)