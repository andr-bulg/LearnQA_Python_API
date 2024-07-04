import requests

payload = {"name": "Andrei", "two": 2}
url = "https://playground.learnqa.ru/api/check_type"
response = requests.patch(url, params=payload)
print(response.text)
print(response.status_code)

