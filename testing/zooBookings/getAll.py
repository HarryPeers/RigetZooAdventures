from sys import path
from os import getcwd
path.append(f"{getcwd()}/../..//site-packages")

import requests
import json

r = requests.get("http://127.0.0.1:80/api/login?email=1&password=1")

print(r.json())

token = r.json()["token"]

r = requests.get("http://127.0.0.1:80/api/bookings/zoo/", headers={"authorization": token})

print(r.text) 