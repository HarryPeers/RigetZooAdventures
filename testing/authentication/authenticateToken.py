from sys import path
from os import getcwd
path.append(f"{getcwd()}/../..//site-packages")

import requests
import json

r = requests.get("http://127.0.0.1:80/api/login", json={"email": "admin", "password": "admin"})

r = r.json()

print(f"token is {r['token']}")

token = r['token']

r = requests.get(f"http://127.0.0.1:80/api/authenticate-token?token={token}")

print(r.text)