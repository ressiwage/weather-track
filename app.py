from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #
import sqlite3
import random, os
import pandas as p
import numpy as np
from grab_cur import get_current as grab_current
from datetime import datetime
import csv
import threading, time



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

def create_db():
    sql = str("""
        CREATE TABLE `days` (
        `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `temperature` int(11) NOT NULL,
        `weather` varchar(250) NOT NULL,
        `humidity` int(11) NOT NULL
        )
        """)
    result = db.engine.execute(sql)

def add_to_db_now(temp, weat, humi):
    sql = str(f"""
        INSERT INTO `days`(
        `id`,
        `temperature`, 
        `weather`, 
        `humidity`,
        `date`) 
        VALUES ({random.randint(1_000_000_000,10_000_000_000)},{temp},'{weat}',{humi},'{datetime.now().replace(microsecond=0)}')
        """)
    result = db.engine.execute(sql)

def clear_db(delete_what):
    sql = str(f"""
        DELETE FROM days {delete_what}
        """)
    result = db.engine.execute(sql)

def select_all():
    sql = str(f"""
        SELECT * FROM days ORDER BY date
        """)
    return [i for i in db.engine.execute(sql)]


class item():
    id = int
    date = str
    temperature = int
    humidity = int
    weather = str
    
    def __repr__(self):
        return '<note %r>' % self.date

    def __init__(self, id, date, temperature, humidity, weather, weather_text=None):
        self.id = id
        self.date = date 
        self.temperature = temperature
        self.humidity=humidity
        self.weather=weather
        self.weather_text=weather_text



#"01-01-2000:[item * 6]"
grouped_items = {}
            
@app.route('/', methods=['GET', 'POST'])
def index():
    #если нет такой даты:
    #   создать такую дату, 6 позиций
    #   вставить на позицию
    #иначе:
    #   вставить на позицию
    
    

    for i in select_all():
        date = datetime.strptime(i[1][2:], '%y-%m-%d %H:%M:%S')
        #i[1] date
        #i[2] temperature
        #i[3] weather
        #i[4] humidity
        if grouped_items.get(str(date.date() ),-1234)==-1234:
            grouped_items.update({ str(date.date() ) : [0]*6})

        print(str(date), date.hour//4, grouped_items)
        grouped_items[str(date.date())][date.hour//4]=item(i[0],i[1],i[2],i[4],"https://"+i[3][2:])
    
    def sort_func(x):
        for i in x:
            if type(i)==item:
                return i
        return 0
    items = sorted([j for i,j in grouped_items.items()], key = lambda x:datetime.strptime(sort_func(x).date[2:], '%y-%m-%d %H:%M:%S').toordinal() ,reverse=True)
    icons=[sort_func(i).weather for i in items]
    headers=[ datetime.strptime(sort_func(i).date[2:], '%y-%m-%d %H:%M:%S').date() for i in items]
    data = grab_current()
    cur_item = item(-1234, datetime.now(),data['temperature'],data['humidity'],data['weather'], weather_text=data['weather_text'])

    if request.method == 'GET':
        if request.args.get('export',-1234)!=-1234:
            header = ['id','date', 'temperature', 'icon', 'humidity']
            data = select_all()
            with open('static/exp.csv', 'w+', encoding='UTF8') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(header)

                # write the data
                for j in data:
                    writer.writerow(j)
            password = request.args.get('password')
            return app.send_static_file("exp.csv")
                
                
    return render_template("index.html", items = items, icons=icons, headers=headers, cur_item=cur_item)

@app.route('/<string:defined_page>')
def custom(defined_page):
    return redirect("/")


@app.route('/page2')
def pg2():
    return render_template("st.html")


if __name__ == '__main__':
    def bd_refresh():
        data = grab_current()
        add_to_db_now(data["temperature"], data["weather"], data["humidity"])
        threading.Timer(60*60, bd_refresh).start()

    threading.Timer(1, bd_refresh).start()
    
    app.run(debug = True)
