from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__)

db = SQLAlchemy()


class books(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
