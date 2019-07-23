import telebot
from app import bot
from app import app
from flask import request


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.bot.process_new_updates([update])
        return ""
    return "<h1>Kore ga Botto da</h1>"
