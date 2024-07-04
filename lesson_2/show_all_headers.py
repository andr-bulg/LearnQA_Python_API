import requests

headers = {"some_header": "123"}
url = "https://playground.learnqa.ru/api/show_all_headers"
response = requests.get(url, headers=headers)
print(response.text)
print(response.headers)

