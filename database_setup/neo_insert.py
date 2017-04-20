import json
import os
from py2neo import Graph, Node, Relationship, NodeSelector
from cosine_sim import cosine_sim

DESCRIPTION_SIMILARITY_THRESHOLD = 0.3
TITLE_SIMILARITY_THRESHOLD = 0.2

PATH = "/home/drogon/Downloads/DatabaseLab/6/test/"
PASSWORD = "generic_password"


def compareText(text1, text2, THRESHOLD):
    similarty_val = cosine_sim(text1, text2)
    if similarty_val > THRESHOLD:
        return similarty_val
    else:
        return 0

print("starting up")

arrayjson = []
filelist = os.listdir(PATH)
for i in range(len(filelist)):
    filelist[i] = PATH + filelist[i]
    page = open(filelist[i], "r")
    parsed = json.loads(page.read())
    arrayjson.append(parsed)

graph = Graph(password=PASSWORD)
transaction = graph.begin()

for i in range(len(arrayjson)):
    arraystring = arrayjson[i]['videoInfo']['statistics']
    a = Node("YoutubeVideos", name=arrayjson[i]['videoInfo']['id'])
    transaction.create(a)
    print("loading file in memory: " + str(i))

selector = NodeSelector(graph)
tnum = -1

for i in range(len(arrayjson)):
    element = arrayjson[i]
    for j in range(i - 1, -1, -1):

        if tnum >= 1000:
            print("1000 transactions in the memory")
            tnum = -1
        if tnum == -1:
            print("commit 1000 transactions")
            transaction.commit()
            transaction = graph.begin()

        if arrayjson[j]['videoInfo']['snippet']['channelId'] == element['videoInfo']['snippet']['channelId']:
            a = selector.select("YoutubeVideos").where(
                name=element['videoInfo']['id']).first()
            b = selector.select("YoutubeVideos").where(
                name=arrayjson[j]['videoInfo']['id']).first()
            channelRelation = Relationship(a, "SAME_CHANNEL", b)
            transaction.create(channelRelation)
            tnum = tnum + 1

        descriptionCount = compareText(
            arrayjson[i]['videoInfo']['snippet']['description'], arrayjson[j]['videoInfo']['snippet']['description'], DESCRIPTION_SIMILARITY_THRESHOLD)
        if descriptionCount:
            a = selector.select("YoutubeVideos").where(
                name=element['videoInfo']['id']).first()
            b = selector.select("YoutubeVideos").where(
                name=arrayjson[j]['videoInfo']['id']).first()
            DescriptionRelation = Relationship(
                a, "SIMILAR_DESC", b, weightage=descriptionCount)
            transaction.create(DescriptionRelation)
            tnum = tnum + 1

        titleCount = compareText(
            arrayjson[i]['videoInfo']['snippet']['title'], arrayjson[j]['videoInfo']['snippet']['title'],
            TITLE_SIMILARITY_THRESHOLD)
        if titleCount:
            a = selector.select("YoutubeVideos").where(
                name=element['videoInfo']['id']).first()
            b = selector.select("YoutubeVideos").where(
                name=arrayjson[j]['videoInfo']['id']).first()
            TitleRelation = Relationship(
                a, "SIMILAR_TITLE", b, weightage=titleCount)
            transaction.create(TitleRelation)
            tnum = tnum + 1

    print("loading relationship in memory: " + str(i))

transaction.commit()
print("done with insertion")
