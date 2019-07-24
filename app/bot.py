import pytz
import requests
import telebot
import re
from app import weather, db
from app.models import User
from config import Config
from time import sleep
from datetime import time, datetime

bot = telebot.TeleBot(Config.TOKEN, threaded=False)
bot.remove_webhook()
sleep(1)
bot.set_webhook(url=Config.HOST_URL)


@bot.message_handler(commands=['start'])
def handle_help(message):
    text_message = "Привет! Это бот для быстрого и удобного просмотра прогноза погоды\n" \
                   "Чтобы начать, установи город. Команды для выбора города:\n" \
                   "/city <название города>\n" \
                   "/city <координаты>\n\n" \
                   "⁉️Советуем первым делом прочитать инструкцию /help"

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(commands=['help'])
def handle_help(message):
    text_message = "*Команды для установки города*\n" \
                   "/city <Имя города> — Через имя\n" \
                   "/city <шырота> <долгота> — Через координаты\n\n" \
                   "Например:\n" \
                   "/city Войнилів\n" \
                   "/city Kiev\n" \
                   "/city 55.7507 37.6177\n" \
                   "/city 55°45′21″  37°37′04″\n\n" \
                   "*Команды для просмотра прогноза погоды*\n" \
                   "/weather — Прогноз на текущий момент\n" \
                   "/weather <n> — Прогноз на n дней\n" \
                   "/detail\_weather — Детальный прогноз\n\n" \
                   "*Настройка напоминаний*\n" \
                   "/notification <время> — Установить на заданое время\n" \
                   "/off — Выключает уведомления\n\n" \
                   "Например:\n" \
                   "/notification 7:00\n" \
                   "/notification 7"

    bot.send_message(message.chat.id, text_message, parse_mode="Markdown")
    print(message.text, message.chat.username)


@bot.message_handler(regexp=r"/weather [\d]+")
def handle_weather_few_days(message):
    pattern = r"/weather [\d]+"
    real_message = re.search(pattern, message.text)[0]

    days_number = real_message.split(" ")[1]
    days_number = "5" if int(days_number) > 5 else days_number

    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        city = user.city
        message_list = weather.get_weather_report(city, int(days_number))
        message_list[0] = message_list[0].replace("N", days_number)

        for msg in message_list:
            bot.send_message(message.chat.id, msg,  parse_mode="Markdown")
    else:
        text_message = "Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>"
        bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp=r"/detail_weather")
def handle_detail_weather(message):
    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        city = user.city
        text_message = weather.detail_weather(city)
    else:
        text_message = "Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>"

    bot.send_message(message.chat.id, text_message, parse_mode="Markdown")
    print(message.text, message.chat.username)


@bot.message_handler(regexp=r"/weather")
def handle_weather(message):
    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        city = user.city
        text_message = weather.get_current_weather(city)
    else:
        text_message = "Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>"

    bot.send_message(message.chat.id, text_message, parse_mode="Markdown")
    print(message.text, message.chat.username)


@bot.message_handler(regexp=r"/city -?[\d]+.?[\d]+ -?[\d]+.?[\d]+")
def handle_city_by_coord(message):
    pattern = r"/city -?[\d]+.?[\d]+[\s]-?[\d]+.?[\d]+"
    real_message = re.search(pattern, message.text)[0].split(" ")

    lat = real_message[1]
    lon = real_message[2]
    city = weather.get_city_by_coord(lat, lon)
    city_name = city['name']
    country = city['country']
    username = message.chat.username

    if city_name:
        text_message = f"Город установлен: {city_name} ({country})"
        user = User.query.filter_by(username=message.chat.username).first()
        if user:
            user.city = city_name
            user.user_chat_id = message.chat.id
            db.session.commit()
        else:
            user = User(username=username, city=city_name, user_chat_id=message.chat.id)
            db.session.add(user)
            db.session.commit()
    else:
        text_message = "В данных координатах нет города"

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp="/city -?[\d]+°[\d]+['′][\d]+[″\"] +-?[\d]+°[\d]+['′][\d]+[″\"]")
def handle_city_by_real_coord(message):
    text_message = "TODO"

    # TODO

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp=r"/city [a-zA-ZА-ї\s]+-?[a-zA-ZА-ї\s]+")
def handle_city_by_name(message):
    pattern = r"/city [a-zA-ZА-ї\s]+-?[a-zA-ZА-ї\s]+"
    city_name = re.search(pattern, message.text)[0][6:]

    city = weather.get_city(city_name)
    username = message.chat.username

    if city[0]:
        text_message = f"Город установлен: {city[0]['name']} ({city[0]['country']})"
        user = User.query.filter_by(username=message.chat.username).first()
        if user:
            user.city = city_name
            user.user_chat_id = message.chat.id
            db.session.commit()
        else:
            user = User(username=username, city=city[0]['name'], user_chat_id=message.chat.id)
            db.session.add(user)
            db.session.commit()
    else:
        text_message = f"Город не найден: {city_name}"

    bot.send_message(message.chat.id, text_message)
    print(message.text, username)


@bot.message_handler(regexp=r"/city")
def handle_city(message):
    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        city = user.city
        text_message = f"Ваш город: {city}\n" \
                       "Изменить город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>\n\n" \
                       "Например:\n" \
                       "/city Войнилів\n" \
                       "/city Kiev\n" \
                       "/city 55.7507 37.6177\n" \
                       "/city 55°45′21″  37°37′04″"
    else:
        text_message = "Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>\n\n" \
                       "Например:\n" \
                       "/city Войнилів\n" \
                       "/city Kiev\n" \
                       "/city 55.7507 37.6177\n" \
                       "/city 55°45′21″  37°37′04″"

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp="/notification [\d]+:[\d]+")
def handle_notification_with_time(message):
    pattern = r"/notification [\d]+:[\d]+"
    real_message = re.search(pattern, message.text)[0].split(" ")[1]

    hours = (real_message.split(":")[0])
    minutes = (real_message.split(":")[1])

    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        if int(hours) >= 24 or int(minutes) >= 60:
            text_message = "Неверный формат времени"
        else:
            local = pytz.timezone("Europe/Kiev")
            now = datetime.now(local)
            print(now)
            notification_datetime = now.replace(hour=int(hours), minute=int(minutes))
            print(notification_datetime)

            requests.get(Config.HOST_URL + "run-tasks/",
                         params={"chat_id": message.chat.id, "notification_time": notification_datetime})

            notification_time = time(int(hours), int(minutes))
            user.notification_time = notification_time
            db.session.commit()
            text_message = f"Напоминание установлено на {hours}:{minutes}"
    else:
        text_message = "Сначала Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>"

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp="/notification [\d]+")
def handle_notification_without_minutes(message):
    pattern = r"/notification [\d]+"
    real_message = re.search(pattern, message.text)[0].split(" ")[1]

    hours = (real_message.split(":")[0])

    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        if int(hours) >= 24:
            text_message = "Неверный формат времени"
        else:
            notification_time = time(int(hours), 0)
            user.notification_time = notification_time
            db.session.commit()
            text_message = f"Напоминание установлено на {hours}:00"
    else:
        text_message = "Сначала Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>"

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp=r"/notification")
def handle_notification(message):
    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        notification_time = str(user.notification_time)[:-3]
        if notification_time:
            text_message = f"Напоминание установлено на {notification_time}\n" \
                           f"Убрать напоминание: /off "
        else:
            text_message = "С помощью уведомлений ты можешь получать в выбранное тобой время прогноз погоды на день\n" \
                           "Например:\n" \
                           "/notification 7:00\n" \
                           "/notification 7"
    else:
        text_message = "Сначала Укажите свой город:\n" \
                       "/city <Имя города>\n" \
                       "/city <шырота> <долгота>"

    bot.send_message(message.chat.id, text_message)
    print(message.text, message.chat.username)


@bot.message_handler(regexp="/off")
def handle_off(message):
    user = User.query.filter_by(username=message.chat.username).first()
    if user:
        user.notification_time = None
        db.session.commit()

    bot.send_message(message.chat.id, "Напоминание снято")
    print(message.text, message.chat.username)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    print(message.text, message.chat.username)
