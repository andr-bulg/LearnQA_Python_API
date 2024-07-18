import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class Test_Get_User(BaseCase):
    def test_get_user_details_not_auth(self):
        url = "https://playground.learnqa.ru/api/user/2"
        response = requests.get(url)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        url_1 = "https://playground.learnqa.ru/api/user/login"
        response_1 = requests.post(url_1, data=data)

        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_1, "user_id")
        url_2 = f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}"

        response_2 = requests.get(url_2, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_2, expected_fields)

