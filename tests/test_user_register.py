import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class Test_User_Register(BaseCase):

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.url = "https://playground.learnqa.ru/api/user/"


    def test_create_user_successfully(self):
        data = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email,
            "password": "123"}

        response = requests.post(self.url, data=data)
        Assertions.assert_code_status(response, 200)
        print(response.content)


    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email,
            "password": "123"}

        response = requests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
               f"content ответа {response.content}"

