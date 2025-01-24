import json
import os
from time import sleep
data={"kk":2,"ss":5}
with open("data.json","w") as f:
    json.dump(data,f)
if os.path.isfile("data.json"):
    with open("data.json","r") as f:
        p=json.load(f)
print(p)