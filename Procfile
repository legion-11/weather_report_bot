web: set FLASK_APP=weather_report_bot.py;
set MAIL_SERVER=smtp.googlemail.com;
set MAIL_PORT=587;
set MAIL_USE_TLS=1;
set MAIL_USERNAME=playersoft1999@gmail.com;
set MAIL_PASSWORD=Levovit1999;
set TOKEN=883081543:AAE7ZUQ8os7qsno4GtjH1Bbn2yuOUk9MNmo
set APPID=5ade4e8d5daf17020d269ca26b52dcd6;
set HOST_URL=https://levovit-weather-bot.herokuapp.com/;
flask db init;
flask db migrate -m "users table";
flask db upgrade;
python weather_report_bot.py -p $PORT