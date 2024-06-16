from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<int:user_id>/posts')
def user_posts(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_posts.html', user=user)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['user_id']
    new_username = request.form['new_username']
    new_email = request.form['new_email']
    user = User.query.get(user_id)
    user.username = new_username
    user.email = new_email
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    content = request.form['content']
    user_id = request.form['user_id']
    post = Post(content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_post', methods=['POST'])
def update_post():
    post_id = request.form['post_id']
    new_content = request.form['new_content']
    post = Post.query.get(post_id)
    post.content = new_content
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_post', methods=['POST'])
def delete_post():
    post_id = request.form['post_id']
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_comment', methods=['POST'])
def add_comment():
    comment_text = request.form['comment']
    post_id = request.form['post_id']
    comment = Comment(text=comment_text, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_comment', methods=['POST'])
def update_comment():
    comment_id = request.form['comment_id']
    new_comment_text = request.form['new_comment']
    comment = Comment.query.get(comment_id)
    comment.text = new_comment_text
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    comment_id = request.form['comment_id']
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)  