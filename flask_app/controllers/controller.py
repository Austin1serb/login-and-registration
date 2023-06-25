from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.model import User
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)



@app.route('/')
def home():

    return render_template('index.html')




@app.route('/create', methods=['POST'])
def create_user():
    print('***************** REQ FORM', request.form)
    if User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
   

    user = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    logged_user = User.create_user(user)
    session['id'] = logged_user
    user = User.get_one_email(user)
    
    return redirect("/")






@app.route('/success')
def success():
    return render_template('success.html')





@app.route('/login', methods=['POST'])
def login():

    data = { "email" : request.form["login_email"] }
    user_in_db = User.get_one_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'user_error')
        return redirect("/")
    elif not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
      
        flash("Invalid Email/Password", 'user_error')
        return redirect('/')
 
    session['id'] = user_in_db.id
    print(session)
    return redirect("/success")



@app.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect('/')