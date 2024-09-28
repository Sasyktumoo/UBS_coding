import json
import logging
from flask import jsonify
from collections import defaultdict

from flask import request

from routes import app

def generate_signatures(word):
    signatures = []
    for i in range(len(word)):
        # Generate signature by removing the i-th character
        signature = word[:i] + word[i+1:]
        signatures.append(signature)
    return signatures

@app.route('/the-clumsy-programmer', methods=['POST'])
def correct_mistypes():
    data_list = request.json

    corrections_list = []

    for data in data_list:
        dictionary = data['dictionary']
        mistypes = data['mistypes']

        # Step 1: Preprocess the dictionary to create a signature map
        signature_map = defaultdict(list)
        
        for word in dictionary:
            signatures = generate_signatures(word)
            for signature in signatures:
                signature_map[signature].append(word)
        
        # Step 2: Correct the mistyped words
        corrections = []
        
        for mistyped_word in mistypes:
            found = False
            mistyped_signatures = generate_signatures(mistyped_word)
            
            for signature in mistyped_signatures:
                possible_words = signature_map.get(signature, [])
                
                # We expect exactly one matching correct word
                if len(possible_words) == 1:
                    corrections.append(possible_words[0])
                    found = True
                    break
            
            if not found:
                # In case no correction is found (shouldn't happen per problem description)
                corrections.append(mistyped_word)
        
        corrections_list.append({"corrections": corrections})

    return jsonify(corrections_list)