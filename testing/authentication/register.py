from sys import path
from os import getcwd
path.append(f"{getcwd()}/../..//site-packages")

import requests
import json

r = requests.post("http://127.0.0.1:80/api/register", json={"email": "harrypeers0606@gmail.com", "password": "happyfeet", "security_question": "What is a table", "security_answer": "white"})

print(r.text)