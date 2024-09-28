import json
import logging
import heapq

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def max_bugsfixed(bugseq):
    bugseq.sort(key=lambda x: x[1])
    
    # heap = []
    # total_time = 0
    
    # for difficulty, limit in bugseq:
    #     heapq.heappush(heap, difficulty)
    #     total_time += difficulty
        
    #     if total_time > limit:
    #         total_time -= heapq.heappop(heap)
    # return len(heap)
    bugseq.sort(key=lambda x: x[1])
    
    total_time = 0
    bugs_fixed = 0
    
    for difficulty, limit in bugseq:
        if total_time + difficulty <= limit:
            total_time += difficulty
            bugs_fixed += 1
    
    return bugs_fixed

@app.route('/bugfixer/p2', methods=['POST'])
def evaluate2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    for item in data:
        bugseq = item.get("bugseq")
        result = max_bugsfixed(bugseq)
        results.append(result)
    logging.info("My result :{}".format(results))
    return json.dumps(results)