from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.parent_suite("Тесты")
@allure.suite("Набор тестов, проверяющих возможность редактировать данные пользователя")
@allure.sub_suite("Сценарии редактирования данных пользователя")

@allure.epic("Сценарии редактирования учётных данных пользователя")
class TestEditUser(BaseCase):

    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.MINOR)
    def test_edit_just_created_user(self):
        """
        Тест на редактирование данных только что созданного пользователя
        """

        # Шаг1: Регистрация нового пользователя
        register_data = self.prepare_registration_data()
        uri_1 = "/user"

        response_1 = MyRequests.post(uri_1, data=register_data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id")

        # Шаг2: Авторизация созданного пользователя
        uri_2 = "/user/login"
        login_data = {
            "email": email,
            "password": password
        }

        response_2 = MyRequests.post(uri_2, data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")

        # Шаг3: Редактирование данных созданного пользователя
        new_name = "Changed Name"
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 200)

        # Шаг4: Получение данных пользователя для проверки того,
        #        что редактирование его данных было выполнено
        response_4 = MyRequests.get(uri_3, headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response_4, "firstName", new_name,
                                             "Неверное имя пользователя после редактирования")


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_without_auth(self):
        """
        Тест на изменение данных только что созданного пользователя
        без авторизации этим пользователем
        """

        # Шаг1: Регистрация нового пользователя
        data = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Шаг2: Попытка редактирования данных пользователя без авторизации этим пользователем
        new_name = "Changed Name"
        uri_2 = f"/user/{user_id}"
        response_2 = MyRequests.put(uri_2, data={"firstName": new_name})

        Assertions.assert_code_status(response_2, 400)
        assert response_2.content.decode("utf-8") == '{"error":"Auth token not supplied"}', \
            f"content ответа {response_2.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_auth_as_existing_static_user(self):
        """
        Тест на изменение данных только что созданного пользователя,
        будучи авторизованными существующим СТАТИЧЕСКИМ пользователем
        """

        # Шаг1: Регистрация нового пользователя
        data = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Шаг2: Выполнение авторизации существующего статического пользователя
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        uri_2 = "/user/login"
        response_2 = MyRequests.post(uri_2, data=login_data)

        # Шаг3: Попытка редактирования данных созданного пользователя
        # с авторизацией существующим статическим пользователем
        new_name = "Changed Name"
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 400)
        assert response_3.content.decode("utf-8") == '{"error":"Please, do not edit test use7rs with ID 1, 2, 3, 4 or 5."}', \
            f"content ответа {response_3.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_auth_as_different_user(self):
        """
        Тест на изменение данных только что созданного пользователя,
        будучи авторизованными другим только что созданным пользователем
        """

        # Шаг1: Регистрация первого пользователя
        data_1 = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data_1)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Шаг2: регистрация и авторизация второго пользователя
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

        # Шаг3: Попытка редактирования данных первого созданного пользователя
        #       с авторизацией вторым созданным пользователем
        new_name = "Changed Name"
        auth_sid = self.get_cookie(response_3, "auth_sid")
        token = self.get_header(response_3, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_4 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_4, 400)
        assert response_4.content.decode("utf-8") == '{"error":"This user can only edit their own data."}', \
            f"content ответа {response_4.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_email_auth_as_same_user(self):
        """
        Тест на изменение email пользователя, будучи авторизованными тем же пользователем,
        на новый email без символа @
        """
        # Шаг1: Регистрация и авторизация пользователя
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

        # Шаг2: Попытка изменения email созданного пользователя на некорректный
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


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user_first_name_auth_as_same_user(self):
        """
        Тест на изменение firstName пользователя, будучи авторизованными тем же пользователем,
        на очень короткое значение в один символ
        """
        # Шаг1: Регистрация и авторизация пользователя
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

        # Шаг2: Попытка изменения firstName созданного пользователя на значение
        # длиной в один символ с авторизацией этого пользователя
        new_name = "A"
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.put(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_3, 400)
        assert response_3.content.decode("utf-8") == '{"error":"The value for field `firstName` is too short"}', \
            f"content ответа {response_3.content}"

