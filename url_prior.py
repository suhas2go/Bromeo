import json
import os
import sqlite3
from database_setup.cosine_sim import cosine_sim


def url_prior(user_id, document):
    conn = sqlite3.connect('database_setup/history.db')
    cursor = conn.execute("SELECT VIDEO_ID, VIDEO_DESC FROM CLICK_THROUGH WHERE USER_ID=?", (user_id,))
    sum = 0
    i = 0
    for row in cursor:
        i += 1
        sum += (cosine_sim(document,row[1]))
    normalized_score = sum/i
    return normalized_score

PATH = "dataset/"
def get_recently_watched(user_id):
    conn = sqlite3.connect('database_setup/history.db')
    cursor = conn.execute("SELECT VIDEO_ID FROM CLICK_THROUGH WHERE USER_ID=?", (user_id,))
    recently_watched = []
    filelist = os.listdir(PATH)
    for i in range(len(filelist)):
        filelist[i] = PATH + filelist[i]
        page = open(filelist[i], "r")
        parsed = json.loads(page.read())
        for r in cursor:
            if r[0]==parsed['videoInfo']['id']:
                recently_watched.append(parsed)
                break

    return recently_watched