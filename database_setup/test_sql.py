from sql_insert import clicked_on_video
import os
import json
import sqlite3

PATH = '../dataset/'
filelist = os.listdir(PATH)
filelist[0] = PATH + filelist[0]
page = open(filelist[0], "r")
video = json.loads(page.read())

clicked_on_video(12, video)
conn = sqlite3.connect('history.db')
cursor = conn.execute("SELECT * FROM CLICK_THROUGH")
print (cursor)
for row in cursor:
    print (row)
    print(row[0],row[1],row[2],row[3])
conn.close()