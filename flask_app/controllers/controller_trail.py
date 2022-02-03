from flask import render_template, redirect, request, session, jsonify
from flask_app import app
from flask_app.models import model_trail, model_review
import os

@app.route('/')
def index():
    all_trails = model_trail.Trail.get_all()
    return render_template('index.html', all_trails=all_trails)

@app.route('/new/trail')
def new_trail():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create-trail.html')

@app.route('/create/trail', methods = ['post'])
def create_trail():
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        **request.form,
        'dog_friendly' : int(request.form['dog_friendly']),
        'user_id' : session['user_id']
    }
    model_trail.Trail.create(data)
    return redirect('/')

@app.route('/edit/trail/<int:id>')
def edit_trail(id):
    if 'user_id' not in session:
        return redirect('/')
    trail = model_trail.Trail.get_one({'id' : id})
    return render_template('edit-trail.html', trail=trail)

@app.route('/trail/<int:id>')
def view_trail(id):
    trail = model_trail.Trail.get_one({'id' : id})
    reviews = model_review.Review.get_all_with_user({'trail_id' : id})
    api_key = os.environ.get("FLASK_APP_API_KEY")
    return render_template('view-trail.html', trail=trail, reviews=reviews, api_key=api_key)

@app.route('/update/trail/<int:id>', methods = ['post'])
def update_trail(id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        **request.form,
        'id' : id,
        'dog_friendly' : int(request.form['dog_friendly']),
        'user_id' : session['user_id']
    }
    model_trail.Trail.update_one(data)
    return redirect('/')


@app.route('/delete/trail/<int:id>')
def delete_trail(id):
    if 'user_id' not in session:
        return redirect('/')
    model_trail.Trail.delete_one({'id' : id})
    return redirect('/')