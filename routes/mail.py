from datetime import datetime, timezone, timedelta
import json
import logging
from flask import jsonify, request
import pytz
from routes import app

logger = logging.getLogger(__name__)

@app.route('/mailtime', methods=['POST'])
def mailtime():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    result = calculate_response_times(data)
    logging.info("My result :{}".format(result))
    
    return json.dumps(result)

def calculate_response_times(data):
    emails = data['emails']
    users = {user['name']: user for user in data['users']}
    
    response_times = {user['name']: [] for user in users.values()}
    
    for i in range(1, len(emails)):
        prev_email = emails[i - 1]
        current_email = emails[i]
        
        sender = current_email['sender']
        receiver = prev_email['receiver']
        
        sender_info = users[sender]
        receiver_info = users[receiver]
        
        prev_time = datetime.fromisoformat(prev_email['timeSent'])
        current_time = datetime.fromisoformat(current_email['timeSent'])

        prev_time = prev_time.astimezone(pytz.timezone(receiver_info['officeHours']['timeZone']))
        current_time = current_time.astimezone(pytz.timezone(sender_info['officeHours']['timeZone']))

        response_seconds = calculate_working_time(prev_time, current_time, sender_info['officeHours'])
        response_times[sender].append(response_seconds)
    
    average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
    
    return {"response": average_response_times}

def calculate_working_time(start, end, office_hours):
    current = start
    total_seconds = 0
    
    while current < end:
        if is_working_hour(current, office_hours):
            next_hour = current + timedelta(hours=1)
            if next_hour > end:
                total_seconds += (end - current).total_seconds()
                break
            total_seconds += 3600
        current += timedelta(hours=1)
        
        if current.hour >= office_hours['end']:
            current += timedelta(days=1)
            current = current.replace(hour=office_hours['start'], minute=0, second=0, microsecond=0)
    
    return total_seconds

def is_working_hour(time, office_hours):
    return office_hours['start'] <= time.hour < office_hours['end'] and time.weekday() < 5