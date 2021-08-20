import RPi.GPIO as pi
import sqlite3 as sql
import tkinter as tk
import time
from flask import Flask , render_template , redirect
import os
from flask_apscheduler import APScheduler
import Adafruit_DHT

pi.setmode(pi.BCM)


#-------------------------------------------
dhtpin=11
delayt = .1 
value = 0 
ldr = 7 

dir = os.path.dirname(os.path.abspath(__file__)) + '/sqldata.db'
DHT_sensor=Adafruit_DHT.DHT11
sensor_humidity, sensor_temperature = Adafruit_DHT.read_retry(DHT_sensor, dhtpin)

app = Flask(__name__)
temp=sensor_temperature
humidity =sensor_humidity
light=0
relay1=0
relay2=0
key=0

def rc_time (ldr):
    count = 0
 
    #Output on the pin for
    Pi.setup(ldr, Pi.OUT)
    Pi.output(ldr, False)
    time.sleep(delayt)
 
    #Change the pin back to input
    Pi.setup(ldr, Pi.IN)
 
    #Count until the pin goes high
    while (Pi.input(ldr) == 0):
        count += 1
 
    return count
 


if humidity is not None and temp is not None:
  print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, humidity))
else:
  print('مشکل دریافت اطلاعات!!!')

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

try:
    # Main loop
    while True:
        print("Ldr Value:")
        value = rc_time(ldr)
        print(value)
        if ( value <= 10000 ):
                print("Lights are ON")
        if (value > 10000):
                print("Lights are OFF")
except KeyboardInterrupt:
    pass
finally:
    Pi.cleanup()

