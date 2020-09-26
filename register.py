from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    name=db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, primary_key=True)
    email=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    time_registered = db.Column(db.DateTime, nullable=False)
