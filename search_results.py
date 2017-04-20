from pymongo import MongoClient
from database_setup.cosine_sim import cosine_sim
from url_prior import url_prior

client = MongoClient()
db = client.youtube
videos = db.videos

CHANNEL_BOOL_THRESHOLD = 0.4


def get_search_results(query, uid):
    video_result = []
    video_dict={}
    for video in videos.find():
        tag_bool = 0
        video_title = video['videoInfo']['snippet']['title']
        video_channel = video['videoInfo']['snippet']['channelTitle']
        try:
            video_tag = video['videoInfo']['snippet']['tags']
        except Exception:
            video_tag = []
        title_wgt = cosine_sim(query, video_title)
        if cosine_sim(query, video_channel) < CHANNEL_BOOL_THRESHOLD:
            channel_bool = 0
        else:
            channel_bool = 1
        for tag in video_tag:
        # tag_bool = cosine_sim(query,tag) --takes a lot of time ,would be better though
            if query.lower() == tag.lower():
                tag_bool = 1
                break

        tag_bool = int(tag_bool)
        content_score = 2 * title_wgt + channel_bool + tag_bool
        weight = 0.7 * content_score + 0.3 * url_prior(uid,video['videoInfo']['snippet']['description'])
        print (weight)
        if weight >= 0.3:
            video_result.append(video)
            video_dict[video['videoInfo']['id']] = weight

    video_result=sorted(video_result, key=lambda video: (video_dict[video['videoInfo']['id']]),reverse=True)
    return video_result
