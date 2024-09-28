from datetime import datetime, timezone, timedelta
import json
import logging
from flask import jsonify, request
import pytz
from routes import app

logger = logging.getLogger(__name__)

def calculate_response_time(emails, users):
    user_data = {user['name']: user for user in users}
    response_times = {user['name']: [] for user in users}
    
    emails.sort(key=lambda x: x['timeSent'])

    for i in range(1, len(emails)):
        email = emails[i]
        prev_email = emails[i - 1]

        if email['subject'].startswith('RE:') and email['receiver'] == prev_email['sender']:
            sender = email['sender']
            sender_info = user_data[sender]
            timezone = pytz.timezone(sender_info['officeHours']['timeZone'])
            
            sent_time = datetime.fromisoformat(email['timeSent']).astimezone(timezone)
            received_time = datetime.fromisoformat(prev_email['timeSent']).astimezone(timezone)
            
            if sent_time <= received_time:
                continue

            start_hour = sender_info['officeHours']['start']
            end_hour = sender_info['officeHours']['end']

            current_time = received_time
            total_seconds = 0

            while current_time < sent_time:
                if current_time.weekday() < 5 and start_hour <= current_time.hour < end_hour:
                    next_hour = min(sent_time, current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
                    total_seconds += (next_hour - current_time).total_seconds()
                    current_time = next_hour
                else:
                    if current_time.hour >= end_hour:
                        current_time = current_time.replace(hour=start_hour, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    else:
                        current_time += timedelta(hours=1)

            response_times[sender].append(total_seconds)

    average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
    return average_response_times

@app.route('/mailtime', methods=['POST'])
def compute():
    try:
        data = request.get_json(force=True)
        #logging.info("Data received for evaluation: {}".format(data))
        
        '''input_data = data.get("input", {})
        emails = input_data.get("emails", [])
        users = input_data.get("users", [])'''

        emails = data.get("emails", [])
        users = data.get("users", [])
        
        result = calculate_response_time(emails, users)
        #logging.info("Calculated response times: {}".format(result))
        
        response = {
            "input": data,
            "output": {
                "response": result
            }
        }
        return jsonify({"response": result})
        #return jsonify(response)
    except Exception as e:
        #logging.error("Error parsing request: {}".format(e))
        return jsonify({"error": "Invalid input"}), 400
