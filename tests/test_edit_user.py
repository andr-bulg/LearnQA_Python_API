import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestEditUser(BaseCase):

    def test_edit_just_created_user(self):
        # Регистрация нового пользователя
        register_data = self.prepare_registration_data()
        url_1 = "https://playground.learnqa.ru/api/user/"

        response_1 = requests.post(url_1, data=register_data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id")

        # Авторизация пользователя
        url_2 = "https://playground.learnqa.ru/api/user/login"
        login_data = {
            "email": email,
            "password": password
        }

        response_2 = requests.post(url_2, data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")

        # Редактирование данных пользователя
        new_name = "Changed Name"
        url_3 = f"https://playground.learnqa.ru/api/user/{user_id}"
        response_3 = requests.put(url_3, headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 200)

        # Получение данных пользователя
        response_4 = requests.get(url_3, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response_4, "firstName", new_name,
                                             "Неверное имя пользователя после редактирования")

