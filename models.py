from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ntrp_level = db.Column(db.String(50), default="NTRP 2.5 (Unverified)")
    skill_score = db.Column(db.Integer, default=0)
    uploaded_video = db.Column(db.String(255), nullable=True)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class RacketListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    seller_contact = db.Column(db.String(100), nullable=False)
