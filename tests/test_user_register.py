from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import string
import random
import allure

@allure.parent_suite("Тесты")
@allure.suite("Набор тестов, проверяющих возможность регистрации пользователя")
@allure.sub_suite("Сценарии регистрации пользователя")

@allure.epic("Сценарии регистрации пользователя")
class Test_User_Register(BaseCase):

    exclude_params = [("no_username"),
                      ("no_firstName"),
                      ("no_lastName"),
                      ("email"),
                      ("password")]

    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 200)
        print("\n", response.content)
        print(response.text)


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
               f"content ответа {response.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_without_symbol_at(self):
        """
        Тест на создание пользователя с некорректным email - без символа @
        """
        email = "some_user_example.com"
        data = self.prepare_registration_data(email)
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"content ответа {response.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_field(self, condition):
        """
        Тест на создание пользователя без указания одного из полей
        """
        data = self.prepare_registration_data()
        uri = "/user"

        if condition == "no_username":
            data.pop("username", None)
            response = MyRequests.post(uri, data=data)
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: username", \
                f"content ответа {response.content}"
        elif condition == "no_firstName":
            data.pop("firstName", None)
            response = MyRequests.post(uri, data=data)
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: firstName", \
                f"content ответа {response.content}"
        elif condition == "no_lastName":
            data.pop("lastName", None)
            response = MyRequests.post(uri, data=data)
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: lastName", \
                f"content ответа {response.content}"
        elif condition == "email":
            data.pop("email", None)
            response = MyRequests.post(uri, data=data)
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: email", \
                f"content ответа {response.content}"
        else:
            data.pop("password", None)
            response = MyRequests.post(uri, data=data)
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: password", \
                f"content ответа {response.content}"


    @staticmethod
    def random_string(length):
        """
        Статический метод, который создаёт и возвращает случайную строку заданной длины
        :param length: длина строки
        :return: случайная строка заданной длины
        """
        symbols = string.ascii_letters + string.digits
        return "".join([random.choice(symbols) for i in range(length)])


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_very_short_firstName(self):
        """
        Тест на создание пользователя с очень коротким именем в один символ
        """
        data = self.prepare_registration_data()
        uri = "/user"
        data["firstName"] = self.random_string(1)

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
            f"content ответа {response.content}"


    @allure.tag("Testing", "Rest API", "Python")
    @allure.label("owner", "Andrei")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_very_long_firstName(self):
        """
        Тест на создание пользователя с очень длинным именем - длиннее 250 символов
        """
        data = self.prepare_registration_data()
        uri = "/user"
        data["firstName"] = self.random_string(251)

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"content ответа {response.content}"

