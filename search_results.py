from pymongo import MongoClient
from pprint import pprint 
from cosine_sim import cosine_sim

client = MongoClient()
db = client.youtube
videos = db.videos

CHANNEL_BOOL_THRESHOLD = 0.4

def get_searchresults(query, uid):
	
	video_result = []
	for video in videos.find():
		tag_bool = 0

		video_title = video['videoInfo']['snippet']['title']
		video_channel = video['videoInfo']['snippet']['channelTitle']
		try:
			video_tag = video['videoInfo']['snippet']['tags']
		except Exception:
			video_tag = []
		title_wgt = cosine_sim(query,video_title)
		if cosine_sim(query,video_channel) < CHANNEL_BOOL_THRESHOLD:
			channel_bool = 0
		else:
			channel_bool = 1
		for tag in video_tag:
			#tag_bool = cosine_sim(query,tag) --takes a lot of time ,would be better though
			if query.lower() == tag.lower():
				tag_bool = 1
				break
		
		tag_bool = int(tag_bool)
		weight = 2*title_wgt+channel_bool+tag_bool
		
		if weight>=0.2:
			video_result.append(video)
	return video_result




