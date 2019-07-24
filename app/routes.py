from datetime import datetime

import telebot
from app import bot, app
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
    notification_time = request.args.get("notification_time")
    print(notification_time)
    if chat_id and notification_time:
        app.apscheduler.add_job(func=scheduled_task, next_run_time=datetime.now().replace(hour=hours, minute=minutes),
                                trigger='interval', seconds=30, args=[chat_id], id=chat_id)

    return 'Scheduled several long running tasks.', 200


def scheduled_task(chat_id):
    bot.bot.send_message(chat_id, "Ima ja")
