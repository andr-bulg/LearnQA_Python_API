from requests import Response
import json


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ представлен не в JSON формате. Текст ответа: {response.text}"

        assert name in response_as_dict, f"Ключ {name} отсутствует в JSON ответе"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ представлен не в JSON формате. Текст ответа: {response.text}"

        assert name in response_as_dict, f"Ключ {name} отсутствует в JSON ответе"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ представлен не в JSON формате. Текст ответа: {response.text}"

        for name in names:
            assert name in response_as_dict, f"Ключ {name} отсутствует в JSON ответе"

    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ представлен не в JSON формате. Текст ответа: {response.text}"

        assert name not in response_as_dict, f"JSON ответ не должен содержать ключ {name}, " \
                                             f"но он присутствует!"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Неожидаемый код ответа! Ожидаемый код: {expected_status_code}. " \
            f"Фактический код: {response.status_code}."

