import sqlite3
from flask import Flask, g, render_template, request, redirect

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
    return render_template("home.html", data=d)

@app.route("/sightings/<string:comname>")
def sightings(comname):
    cur = get_db().cursor()
    select = "SELECT * FROM sightings WHERE sightings.name = '{}' ORDER BY sighted DESC LIMIT 10;".format(comname)
    d = cur.execute(select)
    return render_template("sightings.html", data=d)

@app.route("/update/<string:comname>")
def update(comname):
   return render_template("update.html", c=comname)

@app.route("/update/<string:comname>", methods=['POST'])
def form_update(comname):
    g = request.form['genus']
    s = request.form['species']
    c = request.form['comname']
    cur = get_db().cursor()
    u = cur.execute("UPDATE flowers SET genus='{}', species='{}', comname='{}' WHERE comname='{}'".format(g,s,c,comname))
    get_db().commit()
    return redirect('/home')

@app.route("/insert/<string:comname>")
def insert(comname):
   return render_template("insert.html", c=comname)

@app.route("/insert/<string:comname>", methods=['POST'])
def form_insert(comname):
    p = request.form['person']
    l = request.form['location']
    s = request.form['sighted']
    cur = get_db().cursor()
    temp = "INSERT INTO sightings VALUES ('{}', '{}', '{}', '{}')".format(comname, p, l, s)
    u = cur.execute(temp)
    get_db().commit()
    return redirect('/home')
