import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sslify import SSLify


app = Flask(__name__)
sslify = SSLify(app)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://qmglburntrqick:e184f02ef3f01e928e0ce3d70d77150eef097570a316d1f029ff62bf0628537a@ec2-54-243-208-234.compute-1.amazonaws.com:5432/dc4fumqcquduc"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None

        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None

        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Weather Report Failure',
            credentials=auth, secure=secure)

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/weather_report.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Weather Report startup')


from app import routes, models, bot


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
