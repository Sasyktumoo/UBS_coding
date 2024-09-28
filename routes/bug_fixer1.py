from collections import defaultdict
import json
import logging
from flask import jsonify, request
from routes import app

logger = logging.getLogger(__name__)

@app.route('/bugfixer/p1', methods=['POST'])
def fixer():
    stuff = request.get_json()
    
    class Thing():
        def __init__(self):
            self.before = []
            self.val = None
            
    def createGraph(vals, deps):
        items = defaultdict(Thing)
        x = len(vals)
        
        for i in range(x):
            items[i].val = vals[i]
        
        for a, b in deps:
            items[b - 1].before.append(items[a - 1])
        
        return items
    
    def calc(n):
        if not n.before:
            return n.val
        if n.val is None:
            n.val = max(calc(x) for x in n.before) + n.val
        return n.val
    
    output = []
    
    for thing in stuff:
        vals = thing['time']
        deps = thing['prerequisites']
        
        items = createGraph(vals, deps)
        
        max_val = max(calc(items[i]) for i in range(len(vals)))
        
        output.append(max_val)
    
    return jsonify(output)