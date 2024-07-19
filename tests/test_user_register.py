from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import string
import random


class Test_User_Register(BaseCase):

    exclude_params = [("no_username"),
                      ("no_firstName"),
                      ("no_lastName"),
                      ("email"),
                      ("password")]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 200)


    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
               f"content ответа {response.content}"


    def test_create_user_without_symbol_at(self):
        """
        Создание пользователя с некорректным email - без символа @
        """
        email = "some_user_example.com"
        data = self.prepare_registration_data(email)
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"content ответа {response.content}"


    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_field(self, condition):
        """
        Создание пользователя без указания одного из полей
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


    def test_create_user_with_short_firstName(self):
        """
        Создание пользователя с очень коротким именем в один символ
        """
        data = self.prepare_registration_data()
        uri = "/user"
        data["firstName"] = "A"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
            f"content ответа {response.content}"


    def test_create_user_with_very_long_firstName(self):
        """
        Создание пользователя с очень длинным именем - длиннее 250 символов
        """
        data = self.prepare_registration_data()
        uri = "/user"

        symbols = string.ascii_letters + string.digits
        n = 251
        first_name = "".join([random.choice(symbols) for i in range(n)])
        data["firstName"] = first_name

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"content ответа {response.content}"
