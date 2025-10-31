import sys
import requests

resp = requests.get("http://localhost:5000/")

if resp.status_code != 300:
    sys.exit(1)