import json
import logging
from flask import Flask, jsonify, request
from routes import app

logger = logging.getLogger(__name__)

@app.route('/correct', methods=['POST'])
def correct_words():
    data = request.get_json()
    
    dictionary = data.get("dictionary")
    mistypes = data.get("mistypes")
    corrections = []
    
    for mistyped_word in mistypes:
        for i in range(len(mistyped_word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                candidate = mistyped_word[:i] + c + mistyped_word[i+1:]
                if candidate in dictionary:
                    corrections.append(candidate)
                    break
            else:
                continue
            break

    return jsonify({"corrections": corrections})
