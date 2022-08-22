from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv, os
from grab_cur import get_current as grab_current
from datetime import datetime


app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/sqlite.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres","postgresql")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def create_db():
    sql = str("""
        CREATE TABLE mytable (
        id SERIAL PRIMARY KEY NOT NULL,
        date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        temperature integer NOT NULL,
        weather varchar(250) NOT NULL,
        humidity integer NOT NULL
        )
        """)
    result = db.engine.execute(sql)


def add_to_db_now(temp, weat, humi):
    sql = str(f"""
        INSERT INTO mytable(
        temperature, 
        weather, 
        humidity,
        date) 
        VALUES ({temp},'{weat}',{humi},'{datetime.now().replace(microsecond=0)}')
        """)
    result = db.engine.execute(sql)


def clear_db(delete_what):
    sql = str(f"""
        DELETE FROM mytable {delete_what}
        """)
    result = db.engine.execute(sql)


def select_all():
    sql = str(f"""
        SELECT * FROM mytable ORDER BY date DESC
        """)
    return [i for i in db.engine.execute(sql)]

class item():
    id = int
    date = str
    temperature = int
    humidity = int
    weather = str
    weather_text = str

    def __repr__(self):
        return '<note %r>' % self.date

    def __init__(self, id, date, temperature, weather, humidity, weather_text=None):
        self.id = id
        self.date = date
        self.temperature = temperature
        self.weather = weather
        self.humidity = humidity
        self.weather_text = weather_text


# "01-01-2000:[item * 6]"
grouped_items = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    for i in select_all():
        # i: id, date, temperature, weather, humidity
        date = datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
        if grouped_items.get(str(date.date()), -1234) == -1234:
            grouped_items.update({str(date.date()): [0] * 6})
        print(str(date), date.hour // 4, grouped_items)
        grouped_items[str(date.date())][date.hour // 4] = item(i[0], date, i[2], "https://" + i[3][2:], i[4])

    def sort_func(x):
        for i in x:
            if type(i) == item:
                return i
        return 0

    items = sorted([j for i, j in grouped_items.items()], key=lambda x: sort_func(x).date.toordinal(), reverse=True)
    icons = [sort_func(i).weather for i in items]
    headers = [sort_func(i).date.date() for i in items]
    data = {
        "weather": "cdn.weatherapi.com/weather/64x64/night/113.png",
        "temperature": -1234,
        "humidity": -1234,
        "weather_text": "пробный период на API кончился, так что дальнейшее отслеживание погоды недоступно"
            }
    current_weather = item(-1234, datetime.now(), data['temperature'], data['weather'], data['humidity'],
                    weather_text=data['weather_text'])

    if request.method == 'GET':
        if request.args.get('export', -1234) != -1234:
            header = ['id', 'date', 'temperature', 'icon', 'humidity']
            data = select_all()
            # shutil.copy("lab.db","static/lab.db")
            with open('static/exp.csv', 'w+', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(header)
                # write the data
                for j in data:
                    writer.writerow(j)
            return app.send_static_file("exp.csv")

    return render_template("index.html", items=items, icons=icons, headers=headers, current_weather=current_weather)


@app.route('/<string:defined_page>')
def custom(defined_page):
    return redirect("/")


@app.route('/page2')
def pg2():
    return render_template("st.html")


if __name__ == '__main__':
    #bd_refresh()

    app.run(debug=True)