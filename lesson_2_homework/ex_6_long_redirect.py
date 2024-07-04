import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url)

print("Количество редиректов:", len(response.history))
print("Итоговый URL:", response.url)

