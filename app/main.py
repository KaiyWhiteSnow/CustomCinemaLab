from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/movies/<movie_name>/", methods=["GET", "POST"])
def movie(movie_name:str):
    return render_template("movie.html", movie_name=movie_name)


# Default route for the application
@app.route("/")
def defaultRoute():
    return render_template("index.html")