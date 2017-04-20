import sqlite3
import datetime
import time

'''

    CLICK_THROUGH TABLE
    -----------------------------------------------------------
    | user_id | video_id | video_desc | timestamp | view_count|

'''


def clicked_on_video(user_id, video):
    conn = sqlite3.connect('history.db')
    print("Opened database successfully")
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    '''
    insert_query = "INSERT OR REPLACE INTO CLICK_THROUGH (USER_ID,VIDEO_ID,VIDEO_DESC,TIMESTAMP,CLICK_COUNT) "
    insert_query += "VALUES ('%s','%s','%s','%s'," % (user_id, video['videoInfo']['id'], video['videoInfo']['snippet']['description'], timestamp)
    insert_query += "(SELECT CASE WHEN exists"
    insert_query += "(SELECT 1 FROM CLICK_THROUGH "
    insert_query += "WHERE USER_ID='%s',VIDEO_ID='%s') THEN CLICK_COUNT+1 ELSE 1 END))" % (user_id, video['videoInfo']['id'])
    print (insert_query)
    conn.execute(insert_query)
    '''
    conn.execute("INSERT INTO CLICK_THROUGH (USER_ID,VIDEO_ID,VIDEO_DESC,TIMESTAMP) \
    VALUES (?, ?, ?, ?)", (user_id, video['videoInfo']['id'],video['videoInfo']['snippet']['description'],timestamp))
    conn.commit()
    conn.close()