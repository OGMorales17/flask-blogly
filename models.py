"""Models for Blogly."""
import datetime
from threading import current_thread
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from enum import unique


db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(10), nullable=False, unique=True)
    last_name = db.Column(db.String(10), nullable=False, unique=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user',
                            cascade='all, delete-orphan')

    @property
    def full_name(self):
        """Return full name of user"""
        return f"{self.first_name} {self.last_name}"

# -------------------------  PART TWO  ------------------------------ #


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, default=datetime.datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def date_formatted(self):
        """Return created time formatted"""
        return self.created_at.strftime(" Created on: %a %b %-d %Y, %-I:%M %p")


# -------------------------  PART THREE  ------------------------------ #


class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


def connect_db(app):

    db.app = app
    db.init_app(app)
