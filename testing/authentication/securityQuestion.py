from sys import path
from os import getcwd
path.append(f"{getcwd()}/../..//site-packages")

import requests
import json

r = requests.get("http://127.0.0.1:80/api/security-question", json={"account-email": "h1"})

print(r.text)