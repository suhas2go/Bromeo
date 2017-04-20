import random
from py2neo import Graph, NodeSelector

PASSWORD = "generic_password"

PROB_DESC_RELATION = 1/3
PROB_CHANNEL_RELATION = 1/3
PROB_TITLE_RELATION = 1/3
NUMBER_OF_WALKS = 200
PROB_RESTART = 0.4
CUTOFF_SCORE = 3


def random_walk_with_restart(G,v,alp,n,P,eta):
    vd = v
    counts = {}
    while n > 0:
        if random.random() > alp:
            # need to modify to include weights
            vdd = random.choice(get_neighbours(G, vd))
            selector = NodeSelector(G)
            vd = selector.select("YoutubeVideos").where(name=vdd).first()
            if vd in counts:
                counts[vd] += 1
            else:
                counts[vd] = 1
        else:
            vd = v
        n -= 1

    for k, v in list(counts.items()):
        if v < eta:
            del counts[k]
    return counts


def get_neighbours(graph, node):
    result = graph.run('MATCH (n:YoutubeVideos {name:"%s"})--(m) RETURN m.name' % node["name"]).data()
    neighbours = set()
    for r in result:
        neighbours.add(r["m.name"])
    return list(neighbours)


def get_related_videos(video_id):
    graph = Graph(password=PASSWORD)
    selector = NodeSelector(graph)
    origin_node = selector.select("YoutubeVideos").where(name=video_id).first()
    print (origin_node)
    get_neighbours(graph, origin_node)
    return random_walk_with_restart(graph,origin_node,PROB_RESTART,NUMBER_OF_WALKS,0,CUTOFF_SCORE)
