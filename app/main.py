from flask import Flask, render_template 
from flask_bootstrap import Bootstrap
from routes.offline import Offline
from routes.online import Online, Online

app = Flask(__name__)
app.register_blueprint(Online, url_prefix='/online')
app.register_blueprint(Offline, url_prefix='/offline')
bootstrap = Bootstrap(app)

# Default route for the application
@app.route("/")
def defaultRoute():
    return render_template("index.html")