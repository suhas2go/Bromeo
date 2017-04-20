import flask
from pymongo import MongoClient, ASCENDING

import url_prior
import related_videos
import search_results
import database_setup.sql_insert

app = flask.Flask(__name__)
client = MongoClient()
db = client.youtube
videos = db.videos


def get_related_videos(vid):
    return related_videos.get_related_videos(vid)


def get_trending_videos():
    return videos.find().sort('videoInfo.statistics.viewCount', ASCENDING).limit(24)


def get_recently_watched():
    uid = flask.request.remote_addr
    return url_prior.get_recently_watched(uid)


def get_search_results(query):
    uid = flask.request.remote_addr
    return search_results.get_search_results(query, uid)


def clicked_on_video(vid):
    uid = flask.request.remote_addr
    database_setup.sql_insert.clicked_on_video(uid, vid)


def get_video(vid):
    return videos.find_one({"videoInfo.id": vid})


@app.template_global('url_for_search')
def url_for_search(query):
    return flask.url_for('search') + '?search=' + query + '&action =search'


@app.template_global('url_for_vid')
def url_for_vid(vid):
    return "https://www.youtube.com/embed/" + vid


@app.template_filter('ellipsis')
def ellipsis(text):
    return text[0:600] + "..."


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    if flask.request.method == "GET":
        results = get_trending_videos()
        return flask.render_template("index.html", results=results)


@app.route('/search', methods=["GET"])
def search():
    if flask.request.method == "GET":
        if "search" in flask.request.values:
            query = flask.request.values["search"]
            results = get_search_results(query)
            return flask.render_template("search.html", results=results, query=query)
        else:
            return flask.redirect(flask.url_for('index'))


@app.route('/related/<video_id>', methods=["GET"])
def related(video_id):
    if flask.request.method == "GET":
        video = get_video(video_id)
        results = get_related_videos(video_id)
        clicked_on_video(video_id)
        return flask.render_template("related.html", video=video, results=results)


@app.route('/how', methods=["GET"])
def how():
    return flask.render_template("how.html")


@app.route('/recents', methods=["GET"])
def recents():
    results = get_recently_watched()
    return flask.render_template("recents.html", results=results)


if __name__ == '__main__':
    app.run(debug=True)
