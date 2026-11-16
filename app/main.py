from flask import Flask, render_template


app = Flask(__name__)


@app.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie(movie_name:str):
    return render_template("movie.html", movie_name="/static/movies/"+movie_name)


# Default route for the application
@app.route("/")
def defaultRoute():
    return render_template("index.html")