from . import db
from datetime import datetime
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
from flask_login import UserMixin

    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    about_me = db.Column(db.String(200), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return True if self.admin else False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp,
            'author': self.user_id
        }
        
    def __repr__(self):
        return f'<Post {self.body}>'