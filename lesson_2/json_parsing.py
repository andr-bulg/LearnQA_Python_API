import json

string_as_json_format = '{"answer": "Hello, world!", "one": 1}'
obj = json.loads(string_as_json_format)
key = "answer"
if key in obj:
    print(obj[key])
else:
    print("Ключа {} в JSON нет!".format(key))

