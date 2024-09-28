from collections import defaultdict, deque
import json
import logging
from flask import jsonify, request
from routes import app

logger = logging.getLogger(__name__)

def calculate_total_hours(durations, dependencies):
    num_projects = len(durations)
    
    project_graph = defaultdict(list)
    dependency_count = [0] * num_projects
    project_completion = [0] * num_projects
    
    for prerequisite, dependent in dependencies:
        project_graph[prerequisite - 1].append(dependent - 1)
        dependency_count[dependent - 1] += 1
    
    ready_queue = deque()
    
    for i in range(num_projects):
        if dependency_count[i] == 0:
            ready_queue.append(i)
            project_completion[i] = durations[i]

    while ready_queue:
        current_project = ready_queue.popleft()

        for dependent_project in project_graph[current_project]:
            project_completion[dependent_project] = max(
                project_completion[dependent_project], 
                project_completion[current_project] + durations[dependent_project]
            )
            dependency_count[dependent_project] -= 1
            
            if dependency_count[dependent_project] == 0:
                ready_queue.append(dependent_project)
    
    return max(project_completion)

@app.route('/bugfixer/p1', methods=['POST'])
def project_time():
    data = request.get_json()
    
    results = []
    
    for project_info in data:
        durations = project_info['time']
        dependencies = project_info['prerequisites']
        
        total_hours = calculate_total_hours(durations, dependencies)
        results.append(total_hours)
    
    return jsonify(results)