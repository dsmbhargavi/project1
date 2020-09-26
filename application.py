import os
from sqlalchemy import or_

from flask import Flask,render_template,request,session
# from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
# from sqlalchemy.orm import  sessionmaker

app = Flask(__name__)
a=create_engine("postgres://ijnjabxiugykvh:46457019d5117fecc06ba03fa7a39080893a27b4980e382f0bf60f193fd95587@ec2-34-234-185-150.compute-1.amazonaws.com:5432/d6nvgp7e7umvqn")
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystems
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration",methods=["POST"])
def registration():
    Name=request.form.get("Name")
    UserName = request.form.get("UserName")
    Email=request.form.get("Email")
    Password=request.form.get("Password")
    # print(Name,UserName,Email,Password)
    # return Name+" ,"+Email
     # check if user existed or not
        userData = User.query.filter_by(email=Email).first()

        if userData is not None:
            return render_template("login.html", message="email already exists, Please login.")
        else:
            user = User(name=Name,username=UserName,email=email, password=Password,time_registered=time.ctime(time.time()))

            # check if all details were given for registration.
            try:
                db.session.add(user)
                db.session.commit()
                return name+" ,"+email+","+time_registered
                 # return render_template("user.html",  username=UserName, message="Successfully Registered")

             except:
                 return render_template("registration.html", message="Fill all the details!")
    # return "<h1>Please Register</h1>"


    @app.route("/login",methods=["POST"])
    def login():
            username = request.form.get('username')
            usr_pas = request.form.get('password')

            # check if user existed or not
            userData = User.query.filter_by(username=username).first()

            # if user is present, validate username and password
            if userData is not None:
                if userData.username == username and userData.password == usr_pas:
                    session[username] = username
                    return username;
                    # return redirect(url_for('userHome', user=username))
                # user verification failed
                else:
                    return render_template("registration.html", message="username/password is incorrect!!")
            # if user doesn't exists.
            else:
                return render_template("registration.html", message="Account doesn't exists, Please register!")
        # # if try to access directly
        # else:
        #     return "<h1>Please login/register instead.</h1>"
