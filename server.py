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
        return redirect("/")
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
        return redirect("/")
   except:
        flash("Warehouse exists! Trash!")
        return redirect("/warehouse")

@app.route("/stores")
def stores():
    stores=Store.select().order_by(Store.id)
    return render_template('stores.html',stores=stores)

@app.route('/store/<id_num>')
def show(id_num):
    try:
        store=Store.get_by_id(id_num)
        return render_template('show.html',store=store)
    except:
        flash("No such store! Trash!")
        return redirect("/stores")

@app.route('/edit/<id_num>')
def edit(id_num):
    store=Store.get_by_id(id_num)
    return render_template('edit.html',store=store)

@app.route("/update/<id_num>",methods=["POST"])
def update(id_num):
    update_name = Store.update(name=request.form["chg_store_name"]).where(Store.id == id_num)
    try:
        update_name.execute()
        flash("Name has been changed! :)")
        return redirect("/stores")
    except:
        flash("Attempt unsuccessful! :(")
        return redirect("url_for('update',id_num)")

@app.route("/delete/<id_num>",methods=["POST"])
def delete(id_num):
    store=Store.get_by_id(id_num)
    delete_warehouses = Warehouse.delete().where(Warehouse.store_id == store.id)
    try:
        delete_warehouses.execute()
        store.delete_instance()
        flash("Store has been deleted! :(")
        return redirect("/stores")
    except:
        flash("Attempt unsuccessful! >:(")
        return redirect("/stores")

if __name__ == '__main__':
   app.run()