import time
import requests
import threading


r = requests.post("http://127.0.0.1:8080/api/auth", json={"auth-key": "a6a5cefe-8bef-4041-9506-2f5321fe57a4", "plan": "__dict__"})

print(r)
print(r.text)
    
access_token = r.json()["access_token"]
auth_headers = {
    "Authorization": f"Bearer {access_token}"
}

def f():
    r = requests.get("http://localhost:8080/api/query/earthquake?starttime=2024-01-27", headers=auth_headers)
    print(r.text)
    print(r.json())

# for x in range(5):

f()
time.sleep(.2)

