from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class Test_User_Register(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 200)
        print(response.content)


    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)
        uri = "/user"

        response = MyRequests.post(uri, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
               f"content ответа {response.content}"

