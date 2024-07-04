import requests

payload = {"name": "Andrei"}
url = "https://playground.learnqa.ru/api/hello"
response = requests.get(url, params=payload)
parsed_response_text = response.json()
print(response.text)
print(parsed_response_text["answer"])

