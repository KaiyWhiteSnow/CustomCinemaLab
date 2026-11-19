from flask import Blueprint, render_template, request, url_for, redirect
from PyMovieDb import IMDB
import json
import re


Online = Blueprint('online', __name__)


def _extract_imdb_id(url: str) -> str | None:
    match = re.search(r'tt\d+', url)
    return match.group(0) if match else None


@Online.route("/series/", methods=["GET", "POST"])
def series():
    if request.method == "POST":
        imdb = IMDB()
        series_name = request.form.get("series", "").strip()

        if not series_name:
            return render_template(
                "series_search.html",
                error="Please enter a series name."
            )

        # Search IMDb for TV series
        search_results = json.loads(imdb.search(series_name, tv=True))

        results = search_results.get("results", [])

        if not results:
            return render_template(
                "series_search.html",
                error="Series not found."
            )

        # Get the first matching result
        first_result = results[0]

        imdb_id = first_result.get("id") or _extract_imdb_id(
            first_result.get("url", "")
        )

        if imdb_id:
            print(f"Playing: {first_result['name']} ({imdb_id})")

            return redirect(url_for(
                "online.series_player",
                series_name=series_name,
                season=1,
                episode=1,
                vid_url=f"https://vidsrc.mov/embed/tv/{imdb_id}"
            ))

        return render_template(
            "series_search.html",
            error="Could not retrieve the IMDb ID."
        )

    return render_template("series_search.html")


@Online.route("/series/search/<series_name>/", methods=["GET", "POST"])
def search_series(series_name: str):
    imdb = IMDB()
    json_results = json.loads(imdb.search(series_name, tv=True))

    return json_results


@Online.route("/series/<series_name>/<season>/<episode>/player", methods=["GET", "POST"])
def series_player(series_name: str, season: int, episode: int):
    return render_template("series_player_online.html", series_name=series_name, season=season, episode=episode, vid_url=request.args.get('vid_url'))


@Online.route("/movies/", methods=["GET", "POST"])
def movies():
    if request.method == "POST":
        imdb = IMDB()
        movie = request.form.get("movie")
        json_results = json.loads(imdb.get_by_name(movie))
        id = _extract_imdb_id(json_results['url']) if json_results else None

        if id:
            print(f"Playing the first result: {json_results['name']}")

            return redirect(url_for("online.movie_player", movie_name=movie, vid_url="https://vidsrc.mov/embed/movie/" + id))
        else:
            return render_template("movie_search.html", error="Movie not found.")

    return render_template("movie_search.html")


@Online.route("/movies/search/<movie_name>", methods=["GET", "POST"])
def search_movies(movie_name: str):
    imdb = IMDB()
    json_results = json.loads(imdb.search(movie_name))

    return json_results


@Online.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie_player(movie_name:str):
    return render_template("movie_player_online.html", movie_name=movie_name, vid_url=request.args.get('vid_url'))