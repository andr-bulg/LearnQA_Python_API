import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Создание задачи
response = requests.get(url)

# Получение токена и количества секунд, через сколько задача будет выполнена
response_json = response.json()
token = response_json["token"]
seconds = response_json["seconds"]

# Запрос с token до того как задача готова
response = requests.get(url, params={"token": token})
print(response.text)
# Проверка правильности поля status
assert response.json()["status"] == "Job is NOT ready"

# Ожидание нужного количества секунд, необходимых для выполнения задачи
time.sleep(seconds)

# Запрос с token после того как задача готова
response = requests.get(url, params={"token": token})
print(response.text)
# Проверка правильности поля status и наличия поля result
assert response.json()["status"] == "Job is ready"
assert response.json().get("result", "Поле result отсутствует!") != "Поле result отсутствует!"

