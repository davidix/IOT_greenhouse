import RPi.GPIO as pi
import tkinter as tk
import sqlite3 as sql
import os


dir = os.path.dirname(os.path.abspath(__file__)) + '/sqldata.db'
varlb12 =10
varlb13=1
def create_table():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sqldata (time_ DATETIME , pinkey int )")
    cnt.commit()
    c.close()
    cnt.close()

def getData():
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("SELECT count(pinkey) FROM sqldata  where pinkey=12 ")
    result12 = c.fetchone()
    c.execute("SELECT count(pinkey) FROM sqldata  where pinkey=13 ")
    result13 = c.fetchone()
    lb12.config(text = result12)
    lb13.config(text = result13)
    c.close()
    cnt.close()
    print(result12[0])
    print(result13[0])
    return result12



def inc12():
    create_table()
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("INSERT INTO sqldata VALUES(DATETIME('now'),'12')")
    cnt.commit()
    c.close()
    cnt.close()

def inc13():
    create_table()
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("INSERT INTO sqldata VALUES(DATETIME('now'),'13')")
    cnt.commit()
    c.close()
    cnt.close()
    print(pin)
    
def pinpress(pin):
    create_table()
    cnt = sql.connect(dir)
    c = cnt.cursor()
    c.execute("INSERT INTO sqldata VALUES(DATETIME('now'),:key)",{'key':pin})
    cnt.commit()
    c.close()
    cnt.close()
    print(pin)
    
pi.setmode(pi.BCM)
#pin12
pi.setup(12, pi.IN,pull_up_down=pi.PUD_UP)
pi.add_event_detect(12, pi.FALLING, callback=pinpress, bouncetime=500)
#pin13
pi.setup(13, pi.IN,pull_up_down=pi.PUD_UP)
pi.add_event_detect(13, pi.FALLING, callback=pinpress, bouncetime=500)

win = tk.Tk()
lb12 = tk.Label(win, width=10,height=5,text="varlb12")
lb12.grid(row=1,column=1)
lb13 = tk.Label(win, width=10,height=5,text="varlb13")
lb13.grid(row=2,column=1)
btninc12 = tk.Button(win,width=15,height=10,text="increment lbl 12",command=inc12)
btninc12.grid(row=3,column=1)
btninc13 = tk.Button(win,width=15,height=10,text="increment lbl 13",command=inc13)
btninc13.grid(row=3,column=2)

btn_Show = tk.Button(win,width=30,height=10,text="get Data",command=getData)
btn_Show.grid(row=5,column=1)
win.mainloop()

