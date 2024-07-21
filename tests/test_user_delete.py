from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.parent_suite("Тесты")
@allure.suite("Набор тестов, проверяющих возможность удалить пользователя")
@allure.sub_suite("Сценарии удаления пользователя")

@allure.epic("Сценарии удаления пользователя")
class TestUserDelete(BaseCase):

    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_static_user_auth_as_same_user(self):
        """
        Тест на удаление статического пользователя,
        будучи авторизованным этим пользователем
        """

        # Авторизация статического пользователя
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        uri_1 = "/user/login"
        response_1 = MyRequests.post(uri_1, data=login_data)

        # Попытка удаления статического пользователя с авторизацией под этим пользователем
        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")
        uri_2 = "/user/2"
        response_2 = MyRequests.delete(uri_2, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_2, 400)
        assert response_2.content.decode("utf-8") == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}', \
            f"content ответа {response_2.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_delete_user_auth_as_same_user(self):
        """
        Тест на удаление обычного пользователя,
        будучи авторизованным этим пользователем
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

        # Попытка удаления обычного пользователя с авторизацией под этим пользователем
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_3 = MyRequests.delete(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_3, 200)
        assert response_3.content.decode("utf-8") == '{"success":"!"}', \
            f"content ответа {response_3.content}"

        # Проверка того, что ранее созданный пользователь был удалён
        uri_4 = f"/user/{user_id}"
        response_4 = MyRequests.get(uri_4, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_4, 404)
        assert response_4.content.decode("utf-8") == "User not found", \
            f"content ответа {response_4.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_auth_as_existing_static_user(self):
        """
        Тест на удаление обычного пользователя,
        будучи авторизованным существующим статическим пользователем
        """

        # Создание первого пользователя
        data_1 = self.prepare_registration_data()
        uri_1 = "/user"
        response_1 = MyRequests.post(uri_1, data=data_1)
        Assertions.assert_code_status(response_1, 200)
        user_id = self.get_json_value(response_1, "id")

        # Авторизация существующего статического пользователя
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        uri_2 = "/user/login"
        response_2 = MyRequests.post(uri_2, data=login_data)

        # Попытка удаления созданного пользователя
        # с авторизацией существующим статическим пользователем
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_4 = MyRequests.delete(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_4, 400)
        assert response_4.content.decode("utf-8") == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}', \
            f"content ответа {response_4.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_auth_as_different_user(self):
        """
        Тест на удаление обычного пользователя,
        будучи авторизованным другим обычным пользователем
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

        # Попытка удаления первого пользователя с авторизацией
        # под вторым пользователем
        auth_sid = self.get_cookie(response_3, "auth_sid")
        token = self.get_header(response_3, "x-csrf-token")
        uri_3 = f"/user/{user_id}"
        response_4 = MyRequests.delete(uri_3, headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_4, 400)
        assert response_4.content.decode("utf-8") == '{"error":"This user can only delete their own account."}', \
            f"content ответа {response_4.content}"

