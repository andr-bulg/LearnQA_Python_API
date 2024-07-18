import json
from requests import Response
from datetime import datetime


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Не найден куки {cookie_name} в последнем ответе"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Не найден заголовок {header_name} в последнем ответе"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Ответ представлен не в JSON формате. Текст ответа: {response.text}"

        assert name in response_as_dict, f"Ключ {name} отсутствует в JSON ответе"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
                "username": "learnqa",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "email": email,
                "password": "123"
                }
