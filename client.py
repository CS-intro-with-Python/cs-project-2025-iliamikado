import sys
import requests

OK, ERR, RST = "\033[32m", "\033[31m", "\033[0m"

url = "http://localhost:5000"

def test_existing_page():
    print("::notice::Check existing page 'hello'")
    resp = requests.get(f"{url}/hello")
    if resp.status_code != 200:
        print(f"{ERR}Response status isn't 200")
        print(f"Got {resp.status_code}{RST}")
        sys.exit(1)
    else:
        print(f"{OK}Response code is 200{RST}")

    if resp.content != b"Hello, World!":
        print(f"{ERR}Response content not equal b'Hello, World!'")
        print(f"Got {resp.content}{RST}")
        sys.exit(1)
    else:
        print(f"{OK}Response content is right{RST}")

def test_unexisting_page():
    print("::notice::Check unexisting page")
    resp = requests.get(f"{url}/ssss")
    if resp.status_code != 404:
        print(f"{ERR}Response status isn't 404")
        print(f"Got {resp.status_code}{RST}")
        sys.exit(1)
    else:
        print(f"{OK}Response status is 404{RST}")


test_existing_page()
test_unexisting_page()