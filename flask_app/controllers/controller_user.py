from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import model_user
from flask_app import bcrypt

@app.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')
    
@app.route('/save/user', methods = ['post'])
def create_user():
    if not model_user.User.validate_registration(request.form):
        return redirect('/login') 
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': pw_hash
    }
    user_id = model_user.User.create(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login/user', methods = ['post'])
def login_user():
    if not model_user.User.validate_login(request.form):
        return redirect('/login')
    return redirect('/')


