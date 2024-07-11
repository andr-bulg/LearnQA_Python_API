import requests
import pytest

class Test_User_Auth:

    exclude_params = [("no_cookie"),
                      ("no_token")]

    def setup(self):
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        self.url_1 = "https://playground.learnqa.ru/api/user/login"
        self.url_2 = "https://playground.learnqa.ru/api/user/auth"

        response_1 = requests.post(self.url_1, data=payload)

        assert "auth_sid" in response_1.cookies, "В ответе отсутствует куки аутентификации"
        assert "x-csrf-token" in response_1.headers, "В ответе отсутствует заголовок x-csrf-token"
        assert "user_id" in response_1.json(), "В ответе отсутствует ключ user_id"
        self.auth_sid = response_1.cookies.get("auth_sid")
        self.token = response_1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response_1.json().get("user_id")

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

