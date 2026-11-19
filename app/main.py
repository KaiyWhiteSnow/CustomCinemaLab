from flask import Flask, redirect, render_template, request, url_for 
from flask_bootstrap import Bootstrap
from routes.offline import Offline
from routes.online import Online, Online


app = Flask(__name__)


app.register_blueprint(Online, url_prefix='/online')
app.register_blueprint(Offline, url_prefix='/offline')


# Default route for the application
@app.route("/", methods=["GET", "POST"])
def defaultRoute():
    if request.method == 'POST':
        
        if request.form.get('online'):
            return redirect(url_for("online.movies"))
        
        if request.form.get('offline'):
            return redirect(url_for("offline.movies"))
    
    return render_template("index.html")