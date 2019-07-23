import os

import requests
from config import Config
import time

appid = Config.APPID


def get_city(city_name):
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    if 'list' in data:
        cities = [{'name': d['name'], 'country': d['sys']['country'], 'id': d['id']} for d in data['list']]
    else:
        cities = [{'name': None, 'country': None, 'id': None}]
    return cities


def get_city_by_coord(lat, lon):
    if not -90 <= float(lat) <= 90 and not -180 <= float(lon) <= 180:
        return {'name': None, 'country': None, 'id': None}
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'lat': lat, 'lon': lon, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})

    data = res.json()

    country = data['sys']['country'] if "sys" in data and "country" in data['sys'] else None
    city_name = data['name'] if 'name' in data else None
    city_id = data['id'] if 'id' in data else None

    city = {'name': city_name, 'country': country, 'id': city_id}
    return city


def get_current_weather(city_name):
    city_id = get_city(city_name)[0]['id']
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    condition = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    wind_speed = data['wind']['speed']

    temperature = temp if temp_max == temp_min else f"от {temp_min}ºC до {temp_max}"

    result = f"*Прогноз для:* {city_name}\n" \
             f"*Условие:* {condition}\n" \
             f"*Температура:* {temperature}ºC\n" \
             f"*Скорость ветра:* {wind_speed}"
    return result


def detail_weather(city_name):
    city_id = get_city(city_name)[0]['id']
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    condition = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    wind_speed = data['wind']['speed']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    print(data)

    if hasattr(time, 'tzset'):
        # Move the time zone info into os.environ. See ticket #2315 for why
        # we don't do this unconditionally (breaks Windows).
        os.environ['TZ'] = 'Europe/Kiev'
        time.tzset()

    sunrise = time.strftime("%H:%M", time.localtime(data['sys']['sunrise']))
    sunset = time.strftime("%H:%M", time.localtime(data['sys']['sunset']))
    current_time = time.strftime("%H:%M", time.localtime(data['dt']))

    temperature = temp if temp_max == temp_min else f"от {temp_min}ºC до {temp_max}"

    result = f"*Прогноз для:* {city_name}\n" \
             f"*Условие:* {condition}\n" \
             f"*Температура:* {temperature}ºC\n" \
             f"*Скорость ветра:* {wind_speed} м/с\n" \
             f"*Давление:* {pressure} гПа\n" \
             f"*Влажность:* {humidity}%\n" \
             f"*Рассвет:* {sunrise}\n" \
             f"*Закат:* {sunset}\n" \
             f"*Точное время:* {current_time}\n" \
             f"*Долгота:* {lat}º\n" \
             f"*Широта:* {lon}º"
    return result


def get_weather_report(city_name, days=5):
    city_id = get_city(city_name)[0]['id']
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()

    i = 0
    message_list = list()
    first_date = data['list'][0]['dt_txt']
    if first_date.endswith("00:00:00"):
        message = f"*Прогноз погоды на N дней для:* {city_name}"
    else:
        message_list.append(f"*Прогноз погоды на N дней для:* {city_name}")
        message = f"*0 день* ({first_date[5:7]}/{first_date[8:10]})\n"
    for moment in data['list']:
        date = moment['dt_txt']
        temperature = str(moment['main']['temp'])[:2]
        condition = moment['weather'][0]['description']
        if date.endswith("00:00:00"):
            message_list.append(message)
            message = ""
            i += 1
            if i == days+1:
                break
            message += f"*{i} день* ({date[5:7]}/{date[8:10]})\n"
        message += f"{date[-8:-3]} {temperature}ºC {condition}\n"

    return message_list


if __name__ == '__main__':
    print(detail_weather("Войнилів"))
