import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
payload = {"method": "DELETE"}

response_1 = requests.get(url)
print(response_1.text)

response_2 = requests.head(url)
print(response_2.text)

response_3 = requests.delete(url, params=payload)
print(response_3.text)
print()


payload = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]

for elem in payload:
    response = requests.get(url, params=elem)
    print(f"Тип запроса get, параметр method {elem.get('method')}, ответ: {response.text}")
    response = requests.post(url, data=elem)
    print(f"Тип запроса post, параметр method {elem.get('method')}, ответ: {response.text}")
    response = requests.put(url, data=elem)
    print(f"Тип запроса put, параметр method {elem.get('method')}, ответ: {response.text}")
    response = requests.delete(url, data=elem)
    print(f"Тип запроса delete, параметр method {elem.get('method')}, ответ: {response.text}")
    print()

