import requests, json
from datetime import datetime

endpoint = "http://127.0.0.1:8000/api/new_customer"

data = {
    "tool": [
        '8',
        'my Custom tool'
    ], #done
    "name": "New user", #done
    "phone_number": 1057195554, #done
    "message": "My own note", #done
    "event_type": "My new event type", #done
    "event_place": "Stadium", #done
    "people_count": '555', #done
    "event_date": "2023-11-07T01:12:23.258Z", #done
    "address": "전주시 덕진구 금암1길", #done
    "meal_cost": 30000, #done
}

response = requests.post(f"http://127.0.0.1:8000/api/process_data/64041565", json=data)
print(response.text)