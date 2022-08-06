from grab_cur import get_current as grab_current
import sqlite3, threading, random, datetime
import os, time
from rq import Worker, Queue, Connection


def bd_refresh():
    con = None
    try:
        con = sqlite3.connect("lab2.db")
    except Exception as e:
        print("ERROR",e)

    cur = con.cursor()

    print("iteration")
    data = grab_current()
    sql = "SELECT * FROM `days`"
    sql = f"""
        INSERT INTO days (id, temperature, weather, humidity, date) VALUES (
        {random.randint(1_000_000_000, 10_000_000_000)}, {data["temperature"]}, '{data["weather"]}', {data["humidity"]}, '{datetime.datetime.now().replace(microsecond=0)}');
        """

    print(sql)
    result = cur.execute(sql)
    print(result.fetchall())
    con.commit()
    cur.close()
    con.close()


if __name__ == '__main__':
    while True:
        bd_refresh()
        time.sleep(60)
