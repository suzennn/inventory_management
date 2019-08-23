import peeweedbevolve   #must be imported before models
from flask import Flask, render_template, request, redirect, flash
from models import db, Store, Warehouse

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
   try:
        Store.create(name=store_name)
        flash("Successfully saved!")
        return redirect("/store")
   except:
        flash("Store already exists! Trash!")
        return redirect("/store")

@app.route("/warehouse",methods=["GET"])
def warehouse():
   stores = Store.select()
   return render_template('warehouse.html',stores=stores)

@app.route("/warehouse",methods=["POST"])
def add_warehouse():
   store = Store.get(Store.name == request.form["store_select"])
   w = Warehouse(location=request.form["location"], store=store)
   try:
        w.save()
        flash("Successfully saved!")
        return redirect("/warehouse")
   except:
        flash("Warehouse exists! Trash!")
        return redirect("/warehouse")

@app.route("/stores")
def stores():
   stores=Store.select()
   return render_template('stores.html',stores=stores)

if __name__ == '__main__':
   app.run()