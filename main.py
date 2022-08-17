from flask import Flask, request, render_template, redirect, url_for
import pytube
import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    link = request.form["yt_url"]
    print(link)
    global yt
    try:
        yt = pytube.YouTube(link)
        video_lenght = str(datetime.timedelta(seconds=yt.length))
        views = "{:,}".format(yt.views)
        date = yt.publish_date.strftime("%b %d, %Y")
        for e in yt.streams:
            print(e)
        print("Title: ", yt.title)
        print("Views: ", yt.views)
        print("Length: ", video_lenght)
        return render_template("index.html", display=True, thumb=yt.thumbnail_url, title=yt.title, lenght=video_lenght, views=views, date=date, author=yt.author, description=yt.description, videos=yt.streams)
    except pytube.exceptions.RegexMatchError:
        error = "Please insert a valid YouTube URL."
    except pytube.exceptions.VideoUnavailable:
        error = "That video is no longer available."
    except pytube.exceptions.VideoRegionBlocked:
        error = "That video is region blocked."
    except pytube.exceptions.VideoPrivate:
        error = "That video is private."
    return render_template("index.html", error=error)

@app.route("/download/<string:itag>", methods=["GET", "POST"])
def download_video(itag):
    video = yt.streams.get_by_itag(itag)
    video.download(os.path.expanduser("~/Downloads"), filename_prefix=itag + "-")
    return f"Video {yt.title} successfully downloaded!"
