import requests

def test_check_header_value():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    expected_headers = ['Date', 'Content-Type', 'Content-Length', 'Connection', 'Keep-Alive', 'Server',
                        'x-secret-homework-header', 'Cache-Control', 'Expires']
    actual_headers = list(response.headers.keys())
    assert expected_headers == actual_headers, "Фактический набор заголовков отличается от ожидаемого"

