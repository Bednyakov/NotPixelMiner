from urllib.parse import unquote
import json

url_encoded_str = ""
# Парсинг параметров строки
params = url_encoded_str.split("&")
decoded_params = {}

for param in params:
    key, value = param.split("=")
    decoded_value = unquote(value)
    if key == "user":
        decoded_value = json.loads(decoded_value)
    decoded_params[key] = decoded_value

print(decoded_params)