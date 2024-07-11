import requests
import pytest
class Test_First_API:

    names = ["Andrei", ""]
    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        payload = {"name": name}
        response = requests.get(url, params=payload)
        assert response.status_code == 200, "Неправильный код ответа"

        response_dict = response.json()
        assert "answer" in response_dict, "Ключа answer нет в ответе сервера"

        if not name:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = "Hello, {}".format(name)
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, "Фактический текст ответа неверный!"

