import pytz
import telebot
from datetime import datetime
from app import bot, app, scheduler, weather
from flask import request


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.bot.process_new_updates([update])
        return ""
    return "<h1>Kore ga Botto da</h1>"


@app.route('/run-tasks')
def run_tasks():
    chat_id = request.args.get("chat_id")
    hours = int(request.args.get("hours"))
    minutes = int(request.args.get("minutes"))
    city = request.args.get("city")

    local = pytz.timezone("Europe/Kiev")
    now = datetime.now(local)
    notification_datetime = now.replace(hour=int(hours), minute=int(minutes), second=0)
    if now > notification_datetime:
        notification_datetime = notification_datetime.replace(day=now.day + 1)

    scheduler.add_job(func=scheduled_task, trigger='date', run_date=notification_datetime,
                      args=[chat_id, notification_datetime, city], id=chat_id)
    scheduler.start()

    bot.bot.send_message(chat_id, f"now: {now}\nnotification: {notification_datetime}\nserver time: {datetime.now()}")
    return 'Scheduled several long running tasks.', 200


def scheduled_task(chat_id, notification_datetime, city):
    bot.bot.send_message(chat_id, weather.get_weather_report(city, 0))
    scheduler.add_job(func=scheduled_task, trigger='date', run_date=notification_datetime,
                      args=[chat_id, notification_datetime, city], id=chat_id)
    scheduler.start()
