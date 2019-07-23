# Weather report bot

��� ��� �������� ������

## ��� ������������

�������� � ����������� ����������� ���������

```commandline
virtual venv --python=python3.7
source venv/bin/activate
```
���������� ������ ������
```commandline
pip install flask
pip install flask-sslify
pip install pyTelegramBotAPI
pip install requests
pip install schedule
pip install flask-sqlalchemy
pip install flask-migrate
```
����������� ���� ������
```commandline
flask db init
flask db migrate -m "users table"
flask db upgrade
```
���������� ����������
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
���������� ������ localhost ��� �������
```commandline
ngrok http 5000
set HOST_URL=<your-tunnel-url>
```
� ������� ��������� �� localhost
```commandline
flask run
```
