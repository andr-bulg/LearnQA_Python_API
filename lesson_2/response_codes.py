import requests

response = requests.get("https://playground.learnqa.ru/api/get_500")
print("status_code =", response.status_code)
print(response.text)
print()

response = requests.get("https://playground.learnqa.ru/api/some_method")
print("status_code =", response.status_code)
print(response.text)
print()

response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_response = response.history[0]
second_response = response
print("status_code =", first_response.status_code)
print(first_response.url)
print("status_code =", second_response.status_code)
print(second_response.url)

