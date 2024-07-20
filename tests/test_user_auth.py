import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Сценарии авторизации")
class Test_User_Auth(BaseCase):

    exclude_params = [("no_cookie"),
                      ("no_token")]

    def setup_method(self):
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        self.uri_1 = "/user/login"
        self.uri_2 = "/user/auth"

        response_1 = MyRequests.post(self.uri_1, data=payload)
        self.auth_sid = self.get_cookie(response_1, "auth_sid")
        self.token = self.get_header(response_1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_1, "user_id")

    @allure.description("Тест проверяет успешную авторизацию пользователя c помощью email и пароля")
    def test_user_auth(self):
        response_2 = MyRequests.get(self.uri_2, headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response_2,
                                             "user_id",
                                             self.user_id_from_auth_method,
                                             "user_id_from_auth_method не соответствует user_id_from_check_method")

    @allure.description("Тест проверяет статус авторизации без отправки cookie или token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response_2 = MyRequests.get(self.uri_2, headers={"x-csrf-token": self.token})
        else:
            response_2 = MyRequests.get(self.uri_2, cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response_2,
                                             "user_id",
                                             0,
                                             "Пользователь авторизован с {}".format(condition))

