from grab_cur import get_current as grab_current
import sqlite3, threading, random, datetime
import os, time
from rq import Worker, Queue, Connection



def bd_refresh():
    con = sqlite3.connect("lab2.db")
    cur = con.cursor()
    print(1)
    data = grab_current()
    sql = str(f"""
        INSERT INTO `days`(
        `id`,
        `temperature`, 
        `weather`, 
        `humidity`,
        `date`) 
        VALUES ({random.randint(1_000_000_000,10_000_000_000)},
        {data["temperature"]},
        '{data["weather"]}',
        {data["humidity"]},
        '{datetime.datetime.now().replace(microsecond=0)}')
        """)
    result = cur.executescript(sql)
    
    print(result)

if __name__ == '__main__':
    while True:
        bd_refresh()
        time.sleep(60)
