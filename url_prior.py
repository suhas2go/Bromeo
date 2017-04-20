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