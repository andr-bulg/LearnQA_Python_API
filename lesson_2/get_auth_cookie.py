import requests

payload = {"login": "secret_login", "password": "secret_pass"}
url_1 = "https://playground.learnqa.ru/api/get_auth_cookie"
url_2 = "https://playground.learnqa.ru/api/check_auth_cookie"

response_1 = requests.post(url_1, data=payload)
cookie_value = response_1.cookies.get("auth_cookie")
cookies = {}
if cookie_value:
    cookies.update({"auth_cookie": cookie_value})

response_2 = requests.get(url_2, cookies=cookies)

print(response_1.text)
print(response_1.status_code)
print(dict(response_1.cookies))
print(response_1.headers)
print()
print(response_2.text)

