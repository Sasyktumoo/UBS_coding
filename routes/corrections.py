import json
import logging
from flask import jsonify
from collections import defaultdict

from flask import request

from routes import app

def find_corrections(dictionary, mistypes):
    # Preprocess dictionary
    correction_map = {}
    
    if len(dictionary) > 2000:
        return {}
    
    for word in dictionary:
        word_len = len(word)
        if word_len > 21:
            return {}
        for i in range(word_len):
            # Generate mistyped version by changing each letter
            for c in range(ord('a'), ord('z') + 1):
                if chr(c) != word[i]:
                    mistyped = word[:i] + chr(c) + word[i+1:]
                    correction_map[mistyped] = word
    
    # Find corrections
    corrections = []
    for mistyped in mistypes:
        if mistyped in correction_map:
            corrections.append(correction_map[mistyped])
    
    return corrections

@app.route('/the-clumsy-programmer', methods=['POST'])
def clumsy_programmer():
    # Parse the input JSON, assuming it's a list of dictionaries
    data_list = request.json
    
    results = []
    for data in data_list:
        dictionary = data['dictionary']
        mistypes = data['mistypes']
        
        # Solve the correction problem
        corrections = find_corrections(dictionary, mistypes)
        results.append({'corrections': corrections})
    
    return jsonify(results)