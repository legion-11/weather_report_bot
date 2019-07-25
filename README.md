# Weather report bot

Telegram bot that shows the weather forecast

## How to start
Clone repository
Create and activate a virtual environment

```commandline
virtual venv --python=python3.7
source venv/bin/activate
```
Install the required modules
```commandline
pip install -r requirements.txt
```
Create a database
```commandline
python manage.py db init
python manage.py db migrate -m "users table"
python manage.py db upgrade
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
