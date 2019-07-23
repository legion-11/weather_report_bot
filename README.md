# Weather report bot

Telegram bot that shows the weather forecast

## How to start

Create and activate a virtual environment

```commandline
virtual venv --python=python3.7
source venv/bin/activate
```
Install the required modules
```commandline
pip install flask
pip install flask-sslify
pip install pyTelegramBotAPI
pip install requests
pip install schedule
pip install flask-sqlalchemy
pip install flask-migrate
```
Create a database
```commandline
flask db init
flask db migrate -m "users table"
flask db upgrade
```
Set environment variables
```commandline
set FLASK_APP=weather_report_bot.py
set MAIL_SERVER=smtp.googlemail.com
set MAIL_PORT=587
set MAIL_USE_TLS=1
set MAIL_USERNAME=<your-gmail-username>
set MAIL_PASSWORD=<your-gmail-password>
set TOKEN=<your-token>
set APPID=<your-weather-api-id>
```
Set the tunnel to localhost (https://ngrok.com/download)
```commandline
ngrok http 5000
set HOST_URL=<your-tunnel-url>
```
Run flask on localhost
```commandline
flask run
```
