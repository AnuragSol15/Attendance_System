import json
with open("cred.json") as f:
    cred = json.load(f)
    print(cred)