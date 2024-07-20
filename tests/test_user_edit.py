from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestEditUser(BaseCase):

    def test_edit_just_created_user(self):

        # Регистрация нового пользователя
        register_data = self.prepare_registration_data()
        uri_1 = "/user"

        response_1 = MyRequests.post(uri_1, data=register_data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id")

        # Авторизация пользователя
        uri_2 = "/user/login"
        login_data = {
            "email": email,
            "password": password
        }

        response_2 = MyRequests.post(uri_2, data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")

        # Редактирование данных пользователя
        new_name = "Changed Name"
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 200)

        # Получение данных пользователя
        response_4 = MyRequests.get(uri_3, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response_4, "firstName", new_name,
                                             "Неверное имя пользователя после редактирования")


    def test_edit_just_created_user_without_auth(self):
        """
        Изменение данных пользователя, будучи неавторизованным
        """

        # Создание пользователя
        data = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Попытка редактирования данных пользователя без авторизации
        new_name = "Changed Name"
        uri_2 = f"/user/{user_id}"
        response_2 = MyRequests.put(uri_2, data={"firstName": new_name})

        Assertions.assert_code_status(response_2, 400)
        assert response_2.content.decode("utf-8") == '{"error":"Auth token not supplied"}', \
            f"content ответа {response_2.content}"


    def test_edit_just_created_user_auth_as_different_static_user(self):
        """
        Изменение данных одного пользователя,
        будучи авторизованными другим СТАТИЧЕСКИМ пользователем
        """

        # Создание пользователя
        data = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Авторизация другого статического пользователя
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        uri_2 = "/user/login"
        response_2 = MyRequests.post(uri_2, data=login_data)

        # Попытка редактирования данных созданного пользователя
        # с авторизацией под другим статическим пользователем
        new_name = "Changed Name"
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 400)
        assert response_3.content.decode("utf-8") == '{"error":"Please, do not edit test users with ID 1, 2, 3, 4 or 5."}', \
            f"content ответа {response_3.content}"


    def test_edit_just_created_user_auth_as_different_user(self):
        """
        Изменение данных пользователя, будучи авторизованными другим обычным пользователем
        """

        # Создание первого пользователя
        data_1 = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data_1)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Создание и авторизация второго пользователя
        data_2 = self.prepare_registration_data()
        response_2 = MyRequests.post(uri_1, data=data_2)
        Assertions.assert_code_status(response_1, 200)

        email = data_2["email"]
        password = data_2["password"]
        uri_2 = "/user/login"
        login_data = {
            "email": email,
            "password": password
        }
        response_3 = MyRequests.post(uri_2, data=login_data)

        # Попытка редактирования данных созданного пользователя
        # с авторизацией под другим созданным пользователем
        new_name = "Changed Name"
        auth_sid = self.get_cookie(response_3, "auth_sid")
        token = self.get_header(response_3, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_4 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_4, 400)
        assert response_4.content.decode("utf-8") == '{"error":"This user can only edit their own data."}', \
            f"content ответа {response_4.content}"


    def test_edit_user_email_auth_as_same_user(self):
        """
        Изменение email пользователя, будучи авторизованными тем же пользователем,
        на новый email без символа @
        """
        # Создание и авторизация пользователя
        uri_1 = "/user"
        data = self.prepare_registration_data()
        response_1 = MyRequests.post(uri_1, data=data)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        email = data["email"]
        password = data["password"]
        uri_2 = "/user/login"
        login_data = {
            "email": email,
            "password": password
        }
        response_2 = MyRequests.post(uri_2, data=login_data)

        # Попытка изменения email созданного пользователя на некорректный
        # с авторизацией этого пользователя
        new_email = "some_user_example.com"
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"email": new_email})

        Assertions.assert_code_status(response_3, 400)
        assert response_3.content.decode("utf-8") == '{"error":"Invalid email format"}', \
            f"content ответа {response_3.content}"


    def test_edit_user_first_name_auth_as_same_user(self):
        """
        Изменение firstName пользователя, будучи авторизованными тем же пользователем,
        на очень короткое значение в один символ
        """
        # Создание и авторизация пользователя
        uri_1 = "/user"
        data = self.prepare_registration_data()
        response_1 = MyRequests.post(uri_1, data=data)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        email = data["email"]
        password = data["password"]
        uri_2 = "/user/login"
        login_data = {
            "email": email,
            "password": password
        }
        response_2 = MyRequests.post(uri_2, data=login_data)

        # Попытка изменения firstName созданного пользователя на значение длиной
        # в один символ с авторизацией этого пользователя
        new_name = "A"
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 400)
        assert response_3.content.decode("utf-8") == '{"error":"The value for field `firstName` is too short"}', \
            f"content ответа {response_3.content}"
