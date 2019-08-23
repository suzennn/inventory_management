import peeweedbevolve   #must be imported before models
from flask import Flask, render_template, request, redirect, flash
from models import db, Store
app = Flask(__name__)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store",methods=["GET"])
def store():
   return render_template('store.html')

@app.route("/store",methods=["POST"])
def add_store():
   store_name = request.form["store_name"]
   Store.create(name=store_name)
   flash("Successfully saved!")
#    return redirect("/")

if __name__ == '__main__':
   app.run()