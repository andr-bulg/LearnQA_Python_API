import requests

url = "https://playground.learnqa.ru/api/get_text"
response = requests.get(url)
print(response.text)

