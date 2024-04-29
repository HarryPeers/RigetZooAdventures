from sys import path
from os import getcwd
path.append(f"{getcwd()}/../..//site-packages")

import requests
import json

r = requests.get("http://127.0.0.1:80/api/login?email=h1&password=asd")

print(r.text)