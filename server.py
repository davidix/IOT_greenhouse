import RPi.GPIO as pi
import sqlite3 as sql
import tkinter as tk
import time
from flask import Flask , render_template , redirect
import os
import dht11
#from flask_apscheduler import APScheduler
#import Adafruit_DHT as dht

pi.setmode(pi.BCM)

LIGHT_PIN = 21
pi.setup(LIGHT_PIN, pi.IN)
light = not pi.input(LIGHT_PIN)


#-------------------------------------------
dhtpin=20
delayt = .1 
value = 0 
ldr = 21



dir = os.path.dirname(os.path.abspath(__file__)) + '/sqldata.db'
# DHT_sensor=Adafruit_DHT.DHT11
#sensor_humidity, sensor_temperature = dht.read_retry(dht.DHT11, 20)
sensor_humidity, sensor_temperature = 10,12
instance = dht11.DHT11(pin=20)

dht_res = instance.read()
if dht_res.is_valid():
    s_temp = dht_res.temperature
    s_humidity = dht_res.humidity



app = Flask(__name__)


light=""
relay1=0
relay2=0
key=0
#pin_r1
#pin_r2
pi.setup(17, pi.OUT) 
pi.output(17, 1)

pi.setup(27, pi.OUT) 
pi.output(27, 1)

pi.setup(22, pi.OUT) 
pi.output(22, 1)





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
            pi.output(17, 0)
        elif status=='off':
            relay1 = 0    
            pi.output(17, 1)
            
    elif relay=='2':
        if status=='on':
            relay2 = 1
            pi.output(27, 0)
        elif status=='off':
            relay2 = 0
            pi.output(27, 1)
    elif relay=='3':
        if status=='on':
            light = 1
            pi.output(22, 0)
        elif status=='off':
            light = 0
            pi.output(22, 1)
    insert()    
          




#----------------------------------------
@app.route('/')
def index():
    light = not pi.input(LIGHT_PIN)
    res = get_data()
    print(res)
    

    return render_template('index.html',temp = s_temp, humidity = s_humidity,light= light , relay1=relay1 , relay2 = relay2)

@app.route('/create')
def create():
    create_table()
    return 'Table Create'

@app.route('/<relay>/<status>')
def control_relays(relay,status):
    cnt_rel(relay,status)  
    return redirect('/')  
#-------------------------------------


def scheduleTask():
    print("This test runs every 3 seconds")



if __name__=='__main__':
   # scheduler = APScheduler()
   # scheduler.add_job(func=scheduleTask,id='job',trigger='interval',seconds=10)
   # scheduler.start()
    app.run()






