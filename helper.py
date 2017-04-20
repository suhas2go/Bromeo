import json
import os

folder_name = os.path.dirname(os.path.realpath(__file__)) + "/dataset/"


def get_data():
    data = []
    for filename in os.listdir(folder_name):
        with open(folder_name + filename) as json_file:
            data.append(json.load(json_file))
    return data
