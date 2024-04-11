import time
import random
import requests
import threading


def f(key, x):
    global ks

    #print("making req")
    r = requests.get("http://localhost:8080/api/query/earthquake", params={
        "key": key,
        "starttime": "2024-04-11"
    })
    if r.ok:
        ks[x] += 1
    else:
        print(r.text)

keys = [
    "19efd87b-dd8a-4774-a3e4-b5e599c62b36",
    "eef051b0-bb60-45de-aee3-e170579d30ed"
]

ks = [0, 0]
for i in range(2):
    for x in range(100):
        key = keys[x % 2]
        threading.Thread(target=lambda: f(key, x % 2), daemon=True).start()

input("Waiting >>> ")
print("Expected values")
print(ks)
input(">>> ")
time.sleep(.2)

