import requests

url = "http://downdetector.com/status/apex-legends"

headers = {'Authorization': 'Bearer YOUR_DOWNGRADE_API_KEY'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    status = data["status"]
    if status == "OK":
        print("EA servers are currently up and running.")
    elif status == "ISSUE":
        message = data["message"]
        print(f"EA servers are currently experiencing issues: {message}")
else:
    print("Failed to retrieve server status information.")
