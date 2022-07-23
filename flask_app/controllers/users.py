
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.magazine import Magazine
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods= ['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    register_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id = User.save_user(register_user)
    session['user_id'] = user_id
    flash("You have been registered!", 'register')
    return redirect('/')
    
@app.route('/login', methods= ['POST'])
def login():
    if not User.validate_login(request.form):
        flash("Email not registered!")
        return redirect('/')
    user = User.get_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form["password"]):
            flash("Your Email/Password combination doesn't match", "login")
            return redirect('/')
        session['user_id'] = user.id
        return redirect ('/dashboard')
    flash("Email not Valid!", "login")
    return redirect('/dashboard')


@app.route("/user/account")
def update():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_id(user_data)
    magazines = Magazine.get_all()
    return render_template("edit_account.html", user=user, magazines=magazines)

@app.route("/user/edit/<int:id>", methods = ["POST"])
def update_user(id):
    if User.update_user(request.form):
        User.update(request.form)
        flash("You have been registered!", 'register')
        return redirect('/user/account')
    return redirect ("/user/account")


@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')