web: export FLASK_APP=weather_report_bot.py;
export MAIL_SERVER=smtp.googlemail.com;
export MAIL_PORT=587;
export MAIL_USE_TLS=1;
export MAIL_USERNAME=playersoft1999@gmail.com;
export MAIL_PASSWORD=Levovit1999;
export TOKEN=883081543:AAE7ZUQ8os7qsno4GtjH1Bbn2yuOUk9MNmo
export APPID=5ade4e8d5daf17020d269ca26b52dcd6;
export HOST_URL=https://levovit-weather-bot.herokuapp.com/;
flask db init;
flask db migrate -m "users table";
flask db upgrade;
python weather_report_bot.py -p $PORT