from flask import Blueprint, render_template

Offline = Blueprint('offline', __name__)

@Offline.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie(movie_name:str):
    return render_template("movie.html", movie_name=movie_name)