import sqlite3 as sql
import tkinter as tk
import os

#-------------------------------------------
dir = os.path.dirname(os.path.abspath(__file__)) + '/sqldata.db'

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
#-------------------------------------------
def create_table():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("DROP TABLE IF EXISTS sqldata")
    c.execute("CREATE TABLE sqldata (time_ DATETIME , temp_ FLOAT , humidity FLOAT,light bool)")
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





win = tk.Tk()
win.title("IOT")
lb12 = tk.Label(win, width=10,height=5,text="varlb12")
lb12.grid(row=1,column=1)

lb13 = tk.Label(win, width=10,height=5,text="varlb13")
lb13.grid(row=2,column=1)

btninc12 = tk.Button(win,width=15,height=10,text="increment lbl 12",command= lambda: pinpress("12"))
btninc12.grid(row=3,column=1)

btninc13 = tk.Button(win,width=15,height=10,text="increment lbl 13",command= lambda: pinpress("13"))
btninc13.grid(row=3,column=2)

btn_Show = tk.Button(win,width=30,height=10,text="get Data")
btn_Show.grid(row=5,column=1)
win.mainloop()





