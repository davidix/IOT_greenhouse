import sqlite3 as sql
import tkinter as tk
from flask import Flask , render_template , redirect
import os
from flask_apscheduler import APScheduler

#-------------------------------------------
dir = os.path.dirname(os.path.abspath(__file__)) + '/sqldata.db'
app = Flask(__name__)
temp=20
humidity =30
light=0
relay1=0
relay2=0
key=0

def pinpress(pin):
    create_table()
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("INSERT INTO sqldata VALUES(DATETIME('now'),:key)",{'key':pin})
    cnt.commit()
    c.close()
    cnt.close()
    print(pin)
#------------------------------------
def create_table():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("DROP TABLE IF EXISTS sqldata")
    c.execute("CREATE TABLE sqldata (time_ DATETIME , temp_ FLOAT , humidity FLOAT,light bool,key int)")
    cnt.commit()
    c.close()
    cnt.close()
    
def insert():
    global temp,humidity,light,key
    temp=temp+1
    humidity=humidity+1
    light= not light
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("INSERT INTO sqldata VALUES(DATETIME('now'),:temp_,:humidity,:light,:key)",{'temp_':temp,'humidity':humidity,'light':light,'key':key})
    cnt.commit()
    c.close()
    cnt.close()

def get_data():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("SELECT * FROM sqldata ORDER BY time_ DESC LIMIT 1")
    result = c.fetchone()
    c.close()
    cnt.close()
    return result

def cnt_rel(relay,status):
    global relay1,relay2,light
    if relay=='1':
        if status=='on':
            relay1 = 1
        elif status=='off':
            relay1 = 0    
    elif relay=='2':
        if status=='on':
            relay2 = 1
        elif status=='off':
            relay2 = 0                
    elif relay=='3':
        if status=='on':
            light = 1
        elif status=='off':
            light = 0      
    insert()    
          



#----------------------------------------
@app.route('/')
def index():
    res = get_data()
    print(res)
    return render_template('index.html',temp = int(res[1]) , humidity = int(res[2]),light=str(res[3]) , relay1=relay1 , relay2 = relay2)

@app.route('/create')
def create():
    create_table()
    return 'Table Create'

@app.route('/<relay>/<status>')
def control_relays(relay,status):
    cnt_rel(relay,status)  
    return redirect('/')  
#-------------------------------------



if __name__=='__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=insert,id='job',trigger='interval',seconds=10)
    scheduler.start()
    app.run(debug=True)


