from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class Test_Get_User(BaseCase):
    def test_get_user_details_not_auth(self):
        uri = "/user/2"
        response = MyRequests.get(uri)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        uri_1 = "/user/login"
        response_1 = MyRequests.post(uri_1, data=data)

        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_1, "user_id")
        uri_2 = f"/user/{user_id_from_auth_method}"

        response_2 = MyRequests.get(uri_2, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_2, expected_fields)

    def test_get_user_details_auth_as_different_user(self):
        """
        Тест, который авторизовывается одним пользователем,
        но получает данные другого (т.е. с другим ID)
        """

        # Авторизация первого пользователя
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        uri_1 = "/user/login"
        response_1 = MyRequests.post(uri_1, data=data)

        # Создание второго пользователя
        data = self.prepare_registration_data()
        uri_2 = "/user"
        response_2 = MyRequests.post(uri_2, data=data)
        Assertions.assert_code_status(response_2, 200)

        # Получение данных второго пользователя с авторизацией под первым пользователем
        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_2, "id")
        uri_3 = f"/user/{user_id_from_auth_method}"

        response_3 = MyRequests.get(uri_3, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_json_has_key(response_3, "username")
        Assertions.assert_json_has_no_key(response_3, "email")
        Assertions.assert_json_has_no_key(response_3, "firstName")
        Assertions.assert_json_has_no_key(response_3, "lastName")

