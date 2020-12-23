from flask import Blueprint, request, make_response, jsonify, abort, current_app
from app.models import User, Post
from app import db
from flask_bcrypt import generate_password_hash
import jwt
from datetime import datetime as dt
from datetime import timedelta as td
from functools import wraps


api = Blueprint('api', __name__)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@api.route('/api/v1/posts/', methods=['GET'])
def api_get_posts():
    posts = Post.query.all()
    posts_list = [post.serialize for post in posts]
    return jsonify({'posts': posts_list})


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return func(current_user, *args, **kwargs)
    
    return decorated


@api.route('/api/v1/login/')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
    
    if user.check_password(auth.password):
        token = jwt.encode({
            'id' : user.id,
            'exp': dt.utcnow() + td(minutes=30)},
            current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
    

@api.route('/api/v1/posts/<int:post_id>/', methods=['GET'])
def api_get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return abort(404)
    return jsonify({'post': post.serialize}), 200

@api.route('/api/v1/posts/', methods=['POST'])
@token_required
def api_create_post(current_user):
    req = request.json
    if not req or not 'title' in req\
        or not 'body' in req or not 'author' in req:
        abort(400)

    author_id = req.get('author')
    title = req.get('title')
    body = req.get('body')
    if author_id and author_id.isdigit() and title and body: 
        author = User.query.get(int(author_id))
        if author and author == current_user:
            post = Post(title=title, body=body, author=author)
            db.session.add(post)
            db.session.commit()
            return jsonify({'post': post.serialize}), 201
        else:
            return jsonify({'error': 'Incorrect author'}), 400
    else:
        return jsonify({'error': 'Incorrect data'}), 422

@api.route('/api/v1/posts/<int:post_id>/', methods=['PUT'])
@token_required
def api_update_post(current_user, post_id):
    post = Post.query.get(post_id)
    req = request.json
    if not post:
        abort(404)
    if not req:
        abort(400)
    
    author_id = req.get('author')
    title = req.get('title')
    body = req.get('body')
    if author_id and author_id.isdigit() and title and body:
        author = User.query.get(int(author_id))
        if author and author == current_user:
            post.title = title
            post.body = body
            post.timestamp = dt.utcnow()
            db.session.commit()
            return jsonify({'post': post.serialize}), 200
        else:
            return jsonify({'error': 'Incorrect author'}), 400
    else:
        return jsonify({'error': 'Incorrect data'}), 422

@api.route('/api/v1/posts/<int:post_id>/', methods=['DELETE'])
@token_required
def api_delete_post(current_user, post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    if post.author != current_user:
        return jsonify({'error': 'Cannot perform this action'}), 400

    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True})