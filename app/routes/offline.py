import os

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


def _delete_old_movies():
    """_summary_

    Returns:
        _type_: _description_
    """
    data = json.loads(open("app/static/movies/movie_list.json").read())
    
    for movie in data['movies']:
        if not os.path.exists(f"app/static/movies/{movie['file_name']}"):
            data['movies'].remove(movie)
    
    with open("app/static/movies/movie_list.json", "w") as f:
        json.dump(data, f, indent=4)


def _update_movie_list():
    """_summary_

    Returns:
        _type_: _description_
    """
    data = json.loads(open("app/static/movies/movie_list.json").read())
    data['movies'] = []
    
    for movie in os.listdir("app/static/movies/"):
        if movie.endswith(".mp4"):
            data['movies'].append({
                "movie_name": movie.replace(".mp4", ""),
                "file_name": movie
            })
    
    with open("app/static/movies/movie_list.json", "w") as f:
        json.dump(data, f, indent=4)


@Offline.before_request
def before_first_request():
    _delete_old_movies()
    _update_movie_list()


@Offline.route("/force_update/", methods=["GET", "POST"])
def force_update():
    _delete_old_movies()
    _update_movie_list()
    return redirect(url_for("offline.movies"))


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