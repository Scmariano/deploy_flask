from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.magazine import Magazine
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/dashboard')
def magazines():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_id(data)
    magazines = Magazine.get_all()
    return render_template('dashboard.html', magazines = magazines, user=user)


@app.route("/magazine/new")
def new_magazine():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_id(user_data)
    return render_template("add_magazine.html", user=user)


@app.route("/create/magazine", methods=["POST"])
def create_magazine():
    if not Magazine.validate_magazine(request.form):
        return redirect('/magazine/new')
    Magazine.create(request.form)
    return redirect("/dashboard")

@app.route("/magazine/<int:id>")
def show_magazine(id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_id(user_data)
    magazine_data = {
        'id': id
    }
    magazine = Magazine.get_one(magazine_data)
    return render_template("show_magazine.html", magazine=magazine, user=user)

@app.route("/magazine/<int:id>/delete")
def delete(id):
    magazine_data = {
        'id': id
    }
    Magazine.delete(magazine_data)
    return redirect('/dashboard')

@app.route('/magazine/<int:id>/subscribed', methods=['POST'])
def subscribed(id):
    Magazine.subscribed(request.form)
    return redirect("/dashboard")

@app.route('/magazine/<int:id>/unsubscribed', methods=['POST'])
def unsubscribed(id):
    Magazine.unsubscribed(request.form)
    return redirect("/dashboard")