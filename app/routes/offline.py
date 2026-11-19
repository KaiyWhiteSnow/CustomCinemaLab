from flask import Blueprint, redirect, render_template, url_for, request
import json
from rapidfuzz import fuzz


Offline = Blueprint('offline', __name__)


def _get_movie_by_name(movie_name: str):
    """_summary_

    Args:
        movie_name (str): Query param

    Returns:
        _String_: filename of movie if one is found
    """
    data = json.loads(open("app/static/movies/movie_list.json").read())
    curr_highest = 0
    curr_highest_name = None
            
    for movie in data['movies']:
        if fuzz.WRatio(movie['movie_name'], movie_name) > curr_highest:
            curr_highest = fuzz.WRatio(movie['movie_name'], movie_name)
            curr_highest_name = movie['file_name']
        
    return curr_highest_name


@Offline.route("/movies/", methods=["GET", "POST"])
def movies():
    if request.method == 'POST':
        
        if request.form.get('movie'):
            file_name = _get_movie_by_name(request.form.get('movie'))
            
            return redirect(url_for("offline.movie", movie_name=file_name))
        
    return render_template("movie_search.html")


@Offline.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie(movie_name:str):
    return render_template("movie_player_offline.html", movie_name=movie_name)