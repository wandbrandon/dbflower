import sqlite3
from flask import Flask, g, render_template

#initialize database
DATABASE = 'flowers2019.db'

#Create the app
app = Flask(__name__)

#Getting the database (from documentation)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Closing the database (from documentation)
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
@app.route("/home")
def index():
    cur = get_db().cursor()
    d = cur.execute("SELECT * FROM sightings")
    #h = cur.execute("PRAGMA table_info(sightings);")
    return render_template("index.html", data=d)
