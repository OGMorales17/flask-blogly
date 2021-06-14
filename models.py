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

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(10),
                           nullable=False,
                           unique=True)

    # If no familly member allowed change last_name unique=True
    last_name = db.Column(db.String(10),
                          nullable=False,
                          unique=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user',
                            cascade='all, delete-orphan')

    @property
    def full_name(self):
        """Return full name of user"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)

    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, default=datetime.datetime.now())

    id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)

    @property
    def date_formatted(self):
        """Return created time formatted"""
        return self.created_at.strftime(" Created on: %a %b %-d %Y, %-I:%M %p")


def connect_db(app):

    db.app = app
    db.init_app(app)

# Down this line is what I had to modified

    # @property
    # def date_formatted(self):
    #     """Return created time formatted"""
    #     return "<Example(id=%s, created_at=%s)>" % (self.id, self.created_at)


# class Post(db.Model):
#     __tablename__ = 'posts'

#     post_id = db.Column(db.Integer,
#                         primary_key=True,
#                         autoincrement=True)

#     title = db.Column(db.Text, nullable=False)
#     content = db.Column(db.Text, nullable=False)

#     created_at = db.Column(db.DateTime(timezone=True),
#                            nullable=False, default=datetime.datetime.now())

#     id = db.Column(db.Integer, db.ForeignKey(
#         'users.id'), nullable=False)

#     user = db.relationship('User', backref='posts')
