import requests
import pytest
from lib.base_case import BaseCase

class Test_User_Auth(BaseCase):

    exclude_params = [("no_cookie"),
                      ("no_token")]

    def setup_method(self):
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        self.url_1 = "https://playground.learnqa.ru/api/user/login"
        self.url_2 = "https://playground.learnqa.ru/api/user/auth"

        response_1 = requests.post(self.url_1, data=payload)
        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")


    def test_user_auth(self):
        response_2 = requests.get(self.url_2, headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid})

        assert "user_id" in response_2.json(), "Во втором ответе отсутствует ключ user_id"

        user_id_from_check_method = response_2.json().get("user_id")
        assert self.user_id_from_auth_method == user_id_from_check_method, \
            "user_id_from_auth_method не соответствует user_id_from_check_method"


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response_2 = requests.get(self.url_2, headers={"x-csrf-token": self.token})
        else:
            response_2 = requests.get(self.url_2, cookies={"auth_sid": self.auth_sid})

        assert "user_id" in response_2.json(), "Во втором ответе отсутствует ключ user_id"

        user_id_from_check_method = response_2.json()["user_id"]
        assert user_id_from_check_method == 0, "Пользователь авторизован с {}".format(condition)

