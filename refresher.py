from grab_cur import get_current as grab_current
import sqlite3, threading, random, datetime
import os, time, flask
from flask_sqlalchemy import SQLAlchemy
from rq import Worker, Queue, Connection

db="database"
def init():
    app=flask.Flask(__name__)
    ENV = '!dev'
    if ENV == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/weather'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hzcbtpyfoybsfv:e5ce01b477a6ea7be5cfbee00c122d9f444e0cd83c2504a7faeac19129084e87@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d5sot689t5khc5'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db = SQLAlchemy(app)

def bd_refresh():
    print("iteration")
    data = grab_current()
    sql = "SELECT * FROM `days`"
    sql = f'INSERT INTO days (temperature, weather, humidity, date) VALUES ({data["temperature"]}, "{data["weather"]}", {data["humidity"]}, "{datetime.datetime.now().replace(microsecond=0)}");'
    db.engine.execute(sql)
    print(sql)

if __name__ == '__main__':
    init()
    app.run()
    while True:
        bd_refresh()
        time.sleep(60)
