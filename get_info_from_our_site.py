import requests

url = 'http://localhost:8000/api/forecast/'  # Полный адрес эндпоинта
response = requests.get(url)  # Делаем GET-запрос
# Поскольку данные пришли в формате json, переведем их в python
response_on_python = response.json()
# Запишем полученные данные в файл forecast.txt
with open('forecast.txt', 'w') as file:
    for forecast in response_on_python:
        file.write(forecast['a'])
