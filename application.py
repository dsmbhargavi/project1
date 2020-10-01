import os
from sqlalchemy import or_
import time
from flask import Flask, render_template, request, session, redirect
from register import *
from books import *
# from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
# from sqlalchemy.orm import  sessionmaker

app = Flask(__name__)
# a = create_engine("postgres://ijnjabxiugykvh:46457019d5117fecc06ba03fa7a39080893a27b4980e382f0bf60f193fd95587@ec2-34-234-185150.compute1.amazonaws.com:5432d6nvgp7e7umvqn", echo=True)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

app.secret_key = "qwerty"


@app.route("/")
def index():
    if 'username' in session:
        return render_template("search.html")
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout/<username>")
def logout(username):
    session.pop(username, None)
    return redirect('index.html')


@app.route("/user")
def user():
    return render_template("user.html")


# @app.route("/search")
# def search():
 #   return render_template("search.html")


@app.route("/admin/<user>")
def admin(user):
    if user in session and user == "Bunny":
        users = User.query.all()
        return render_template("admin.html", users=users)
    return render_template('login.html', message="Please login!!")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        Name = request.form.get("Name")
        UserName = request.form.get("UserName")
        Email = request.form.get("Email")
        Password = request.form.get("Password")
        userData = User.query.filter_by(email=Email).first()

        if userData is not None:
            return render_template("login.html", message="email already exists, Please login.")
        else:
            user = User(name=Name, username=UserName, email=Email,
                        password=Password, time_registered=time.ctime(time.time()))
            print("user creation done")

            # print(db.session.queryall)
            # print(user.queryall)

            # check if all details were given for registration.
            try:
                db.session.add(user)
                db.session.commit()
                return render_template("user.html",  username=UserName, message="Successfully Registered")
            except:
                return render_template("index.html", message="Fill details!")
        return render_template("index.html", message="Register")


@app.route("/ldetails", methods=["POST", "GET"])
def ldetails():
    if request.method == "POST":
        username = request.form.get('username')
        userpass = request.form.get('password')
        userData = User.query.filter_by(username=username).first()
        if userData is not None:
            if userData.username == username and userData.password == userpass:
                session[username] = username
                return render_template("search.html", user=username, message="Sucess")
            else:
                return render_template("login.html", message="details incorrect!!")
        else:
            return render_template("index.html", message="Account doesn't exists, Go to Registration")
    else:
        return render_template("login.html")


@ app.route("/search/<user>", methods=["POST", "GET"])
def search(user):
    if request.method == "GET":
        # return render_template("Search.html", user = user)
        return redirect('index.html')

    else:
        res = request.form.get("find")
        res = '%'+res+'%'
        result = books.query.filter(or_(books.title.ilike(
            res), books.author.ilike(res), books.isbn.ilike(res))).all()
        return render_template("search.html", result=result, user=user)
