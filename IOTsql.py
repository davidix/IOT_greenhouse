import sqlite3 as sql
from flask import Flask
import os
#from flask_apscheduler import APScheduler

dir = os.path.dirname(os.path.abspath(__file__)) + '/datasql.db'
app = Flask(__name__)

temp = 20
humidity = 40

def create():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("DROP TABLE IF EXISTS datasql")
    c.execute("CREATE TABLE datasql (time_ DATETIME , temp_ FLOAT , humidity FLOAT)")
    c.close()
    cnt.close()


def insert():
    global temp,humidity
    temp = temp +1
    humidity = humidity+1
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("INSERT INTO datasql VALUES(DATETIME('now'),:temp_,:humidity)",{'temp_':temp , 'humidity':humidity})
    cnt.commit()
    c.close()
    cnt.close()

def get_data():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("SELECT * FROM datasql ORDER BY time_ DESC LIMIT 1")
    result = c.fetchone()
    c.close()
    cnt.close()
    return result

@app.route('/create')
def create_table():
    create()
    return 'Table Create'

@app.route('/')
def index():
    result = get_data()
    if not result:
        return 'No Data'
    else:
        return 'Last update time ={0} <br>   Temperature ={1}  <br>   Humidity ={2} '.format(result[0],result[1],result[2])


if __name__=='__main__':
    # scheduler = APScheduler()
    # scheduler.add_job(func=insert,id='job',trigger='interval',seconds=10)
    # scheduler.start()
    app.run(debug=True)

