import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class Test_User_Register(BaseCase):

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email,
            "password": "123"}

        url = "https://playground.learnqa.ru/api/user/"

        response = requests.post(url, data=data)
        assert response.status_code == 400, f"Статус код равен {response.status_code}"
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
               f"content ответа {response.content}"
        # print(response.status_code)
        # print(response.content)

