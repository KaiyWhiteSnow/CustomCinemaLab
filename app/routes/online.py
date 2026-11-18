from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from PyMovieDb import IMDB
import json
import re


imdb = IMDB()
Online = Blueprint('online', __name__)


def _extract_imdb_id(url: str) -> str | None:
    match = re.search(r'tt\d+', url)
    return match.group(0) if match else None

@Online.route("/movies/", methods=["GET", "POST"])
def movies():
    if request.method == "POST":
        movie = request.form.get("movie")
        json_results = json.loads(imdb.get_by_name(movie))
        id = _extract_imdb_id(json_results['url']) if json_results else None
        if id:
            print(f"Playing the first result: {json_results['name']}")
            return redirect(url_for("online.movie_player", movie_name=movie, vid_url="https://vidsrc.mov/embed/movie/" + id))
        else:
            return render_template("movie_search.html", error="Movie not found.")
    return render_template("movie_search.html")


@Online.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie_player(movie_name:str):
    return render_template("movie_player_online.html", movie_name=movie_name, vid_url=request.args.get('vid_url'))


@Online.route("/series/<series_name>/<season>/<episode>/", methods=["GET", "POST"])
def series(series_name:str, season:int, episode:int):
    return render_template("series.html", series_name=series_name, season=season, episode=episode)
