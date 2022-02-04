from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models import model_review, model_trail

@app.route('/new/review/<int:id>')
def new_review(id):
    if 'user_id' not in session:
        return redirect('/')
    trail = model_trail.Trail.get_one({'id' : id})
    return render_template('create-review.html', trail=trail)

@app.route('/create/review/<int:id>', methods = ['post'])
def create_review(id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        **request.form,
        'user_id' : session['user_id'],
        'trail_id' : id
    }
    model_review.Review.create(data)
    return redirect('/')

@app.route('/edit/review/<int:id>')
def edit_review(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    review = model_review.Review.get_one_with_trail(data)
    return render_template('edit-review.html', review = review)

@app.route('/update/review/<int:id>', methods = ['post'])
def update_review(id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        **request.form,
        'id' : id,
    }
    model_review.Review.update_one(data)
    return redirect(url_for('view_trail', id=request.form['trail_id']))

@app.route('/delete/review/<int:id>', methods=['post'])
def delete_review(id):
    if 'user_id' not in session:
        return redirect('/')
    model_review.Review.delete_one({'id':id})
    return redirect(url_for('view_trail', id=request.form['trail_id']))
