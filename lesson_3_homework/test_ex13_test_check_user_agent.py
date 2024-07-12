import requests
import pytest

user_agent_1 = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}
user_agent_2 = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"}
user_agent_3 = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
user_agent_4 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"}
user_agent_5 = {"User-Agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}

expected_values = [{'platform': 'Mobile', 'browser': 'No', 'device': 'Android'},
                   {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'},
                   {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'},
                   {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'},
                   {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}]

dataset = [(user_agent_1, expected_values[0]),
        (user_agent_2, expected_values[1]),
        (user_agent_3, expected_values[2]),
        (user_agent_4, expected_values[3]),
        (user_agent_5, expected_values[4])]

@pytest.mark.parametrize('data', dataset)
def test_check_user_agent(data):
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    header = data[0]
    response = requests.get(url, headers=header)
    expected_value = data[1]

    assert expected_value["platform"] == response.json()["platform"], \
         "User-Agent {!r} имеет неправильный параметр platform {!r}".format(response.json()['user_agent'], response.json()["platform"])
    assert expected_value["browser"] == response.json()["browser"], \
        "User-Agent {!r} имеет неправильный параметр browser {!r}".format(response.json()['user_agent'], response.json()['browser'])
    assert expected_value["device"] == response.json()["device"], \
        "User-Agent {!r} имеет неправильный параметр device {!r}".format(response.json()['user_agent'], response.json()['device'])

