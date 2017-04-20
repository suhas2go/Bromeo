import json
import os
from pprint import pprint

from pymongo import MongoClient

client = MongoClient()
db = client.youtube
videos = db.videos

folder_name = "../dataset/"

for filename in os.listdir(folder_name):
    print("storing", filename)
    with open(folder_name + filename) as json_file:
        data = json.load(json_file)
        # convert like count string to int for better queryeing
        try:
            data["videoInfo"]["statistics"]["likeCount"] = int(data["videoInfo"]["statistics"]["likeCount"])
        except Exception:
            pass
        
        videos.insert_one(data)