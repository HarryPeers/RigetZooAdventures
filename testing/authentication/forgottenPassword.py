from sys import path
from os import getcwd
path.append(f"{getcwd()}/../..//site-packages")

import requests
import json

email = "h1"

r = requests.get("http://127.0.0.1:80/api/security-question", json={"account-email": "h1"})

print(r.text)

f = input("")

r = requests.post("http://127.0.0.1:80/api/security-question", json={"account-email": "h1", "security-answer": f})

print(r.text)
t = r.json()["token"]

new = input("New password: ")

r = requests.put("http://127.0.0.1:80/api/forgotten-password", json={"token": t, "new-password": new})

print(r.text)