"""import threading, sqlalchemy
from flask_sqlalchemy import SQLAlchemy #
#from grab_cur import get_current as grab_current
#from app import add_to_db_now
import os

db = SQLAlchemy(app)

def create_db():
    sql = 
    result = db.engine.execute(sql)

def bd_refresh():
    print (os.path.abspath(os.path.join(os.path.abspath(os.getcwd()), os.pardir)))
    print (os.path.abspath(os.getcwd()))
    print(1)
    data = grab_current()
    add_to_db_now(data["temperature"], data["weather"], data["humidity"])
    threading.Timer(10, bd_refresh).start()
    
threading.Timer(1, bd_refresh).start()"""