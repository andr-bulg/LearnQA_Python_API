import requests

def test_check_cookie_value():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    expected_cookie = "hw_value"
    actual_cookie = response.cookies.get("HomeWork")
    assert expected_cookie == actual_cookie, "Фактическое значение cookie отличается от ожидаемого"

