from flask import Blueprint, redirect, render_template, url_for, request

Offline = Blueprint('offline', __name__)

@Offline.route("/movies/", methods=["GET", "POST"])
def movies():
    if request.method == 'POST':
        if request.form.get('movie'):
            return redirect(url_for("offline.movie", movie_name=request.form.get('movie')))
    return render_template("movie_search.html")

@Offline.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie(movie_name:str):
    return render_template("movie_player_offline.html", movie_name=movie_name)