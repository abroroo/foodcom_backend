import requests, json
from datetime import datetime

endpoint = "http://127.0.0.1:8000/api/new_customer"

data = {
    "tool": [
        '11'
    ],
    "customTool": "MyTool", #done
    "name": "New user", #done
    "phone_number": 1057195554, #done
    "message": "My own note", #done
    "event_type": "My new event type", #done
    "event_place": "Stadium", #done
    "people_count": '555', #done
    "event_date": "2023-11-29T15:00:00.000Z", #done
    "event_time" : "17:05",
    "address": "전주시 덕진구 금암1길", #done
    "meal_cost": 30000, #done
}

{"address":"전북 전주시","tool":["11","3","4","12"],"customTool":"","event_type":"festival","date_rigistered":"2023-12-14T19:57:01.513Z","event_date":"2023-12-26T15:00:00.000Z","event_time":"00:00","meal_cost":55000,"event_place":"연회장","name":"ㅇㅀㄴㅇㅀ","phone_number":32423423433,"message":"dfasfds","people_count":"410"}

response = requests.post(f"http://127.0.0.1:8000/api/process_data/13526773", json=data)
print(response.text)