from grab_cur import get_current as grab_current
import datetime
import os, time, flask
from flask_sqlalchemy import SQLAlchemy

offset = datetime.timedelta(hours=5)
tz = datetime.timezone(offset, name='ЕКТ')

def bd_refresh():
    global db
    print("iteration of refresher")
    data = grab_current()
    sql = f"""INSERT INTO days (
    temperature, weather, humidity, date
    ) VALUES (
    {data["temperature"]}, '{data["weather"]}', {data["humidity"]}, '{datetime.datetime.now(tz=tz).replace(microsecond=0)}'
    );"""
    db.engine.execute(sql)
    print(sql)

if __name__ == '__main__':
    app = flask.Flask(__name__)
    ENV = '!dev'
    if ENV == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/weather'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    while True:
        bd_refresh()
        time.sleep(60*60)
