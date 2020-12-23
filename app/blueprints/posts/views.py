from flask import Blueprint, redirect, request, render_template, flash, url_for, current_app
from app.models import User, Post
from app import db
from app.forms import CreatePostForm, UpdatePostForm
from flask_login import login_required, current_user
from datetime import datetime

pb = Blueprint('posts', __name__, template_folder='templates')


@pb.route('/posts/', methods=['GET'])
def posts():
    query = request.args.get('q')
    
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.body.contains(query))
    else:
        posts = Post.query.order_by(Post.timestamp.desc())
    posts_per_page = current_app.config['POSTS_PER_PAGE']
    pages = posts.paginate(page=page, per_page=posts_per_page)
    return render_template('posts/posts.html', posts=posts, pages=pages, query=query)


@pb.route('/posts/new/', methods=['GET', 'POST'])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        post = Post(title=title, body=body, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Nice post, but you can better', 'success')
        return redirect(url_for('posts.posts'))

    return render_template('posts/create_post.html', form=form)


@pb.route('/posts/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    return render_template('posts/post.html', post=post)


@pb.route('/posts/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if current_user != post.author:
        flash('You don\'t have enough rights to update this post', 'warning')
        return redirect(url_for('posts.posts'))  
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.timestamp = datetime.utcnow()
        db.session.commit()
        flash('I like it better now!', 'success')
        return redirect(url_for('posts.update_post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    return render_template('posts/update_post.html', form=form, post=post)


@pb.route('/posts/<int:post_id>/delete/')
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    if current_user != post.author:
        flash('You don\'t have enough rights to delete this post', 'warning')  
    else:
        title = post.title
        db.session.delete(post)
        db.session.commit()
        flash(f'Post {title} was deleted!', 'success')
    return redirect(url_for('posts.posts'))