import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TOKEN = os.environ.get('TOKEN') or "883081543:AAE7ZUQ8os7qsno4GtjH1Bbn2yuOUk9MNmo"
    HOST_URL = os.environ.get('HOST_URL') or "https://levovit-weather-bot.herokuapp.com/"
    APPID = os.environ.get('APPID') or "5ade4e8d5daf17020d269ca26b52dcd6"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['playersoft1999@gmail.com']
