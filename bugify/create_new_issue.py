import requests

# Создание нового баг-репорта

payload = {"subject": "new_issue", "description": "New issue was created"}
username = "4ca3f6634f7e1244134ab16f7f444295"
password = ""
url = "https://bugify.stqa.ru/api/issues.json"

response = requests.post(url, data=payload, auth=(username, password))
assert response.status_code == 201, "Вернулся неверный код ответа!"
assert response.json()["message"] == "Issue has been created.", "Баг-репорт не был создан!"


# Просмотр только что созданного баг-репорта
issue_id = response.json()["issue_id"]
url = "https://bugify.stqa.ru/api/issues/{}.json".format(issue_id)
response = requests.get(url, auth=(username, password))
assert response.status_code == 200, f"Вернулся неверный код ответа! Баг-репорт {issue_id} не найден!"
print(f"Issue {issue_id}:")
print(response.text)
