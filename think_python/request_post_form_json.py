
import requests

form_data = {'name': 'Matthew', 'sex': 'M', 'age': 25}

#r = requests.post("http://127.0.0.1:5000/process_form", data=form_data,)

r = requests.post("http://127.0.0.1:5000/process_json", json=form_data,)

print(r.text)