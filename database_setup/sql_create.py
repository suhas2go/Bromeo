import sqlite3

conn = sqlite3.connect('history.db')
conn.execute('''CREATE TABLE CLICK_THROUGH
       (USER_ID TEXT NOT NULL,
       VIDEO_ID TEXT NOT NULL,
       VIDEO_DESC TEXT,
       TIMESTAMP TEXT,
       PRIMARY KEY(USER_ID,VIDEO_ID,TIMESTAMP));''')
conn.close()