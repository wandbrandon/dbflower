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
    d = cur.execute("SELECT * FROM flowers") 
    return render_template("index.html", data=d)

@app.route("/sightings/<string:comname>")
def sightings(comname):
    cur = get_db().cursor()
    select = "SELECT * FROM sightings WHERE sightings.name = '{}' ORDER BY sighted DESC LIMIT 10;".format(comname)
    d = cur.execute(select)
    return render_template("sightings.html", data=d)

