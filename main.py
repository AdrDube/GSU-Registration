from flask import request, render_template, Flask, url_for, redirect, session, flash
from validity import valid_web, valid_works
from courses import get_transcripts, get_degree_info
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from functools import wraps
from dotenv import dotenv_values
from mySQL import taken_info, get_remaining
from cryptography.fernet import Fernet
import sys
app = Flask("My app")
secrets = dotenv_values(".env")

cipher = Fernet(secrets["cipher"].encode('utf-8'))

host = secrets["mysql_host"]
user = secrets["mysql_user"]
password = secrets["mysql_password"]
database = secrets["mysql_database"]
port = secrets["port"]

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

app.secret_key = secrets["secret_key"]

login=LoginManager()
login.__init__(app)
db=SQLAlchemy(app)

class Student(UserMixin, db.Model):
    __tablename__ = 'students'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30)) 
    password= db.Column(db.String(100))
    g_num= db.Column(db.String(100))
    web_pin= db.Column(db.String(100))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for(login))
        return f(*args, **kwargs)
    return decorated_function

@login.user_loader
def load_user(user):
    return Student.query.get(user)



@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = data["password"]
        user = Student.query.filter_by(username=username).first()
        if user and password == cipher.decrypt(user.password).decode():
            login_user(user)
            flash("Successful. Logging in...", "success") 
            return render_template('index.html',login=True, redirect_target=url_for('homepage'))
        flash("Invalid login details. Try again", "error")

    return render_template("index.html", login=True)




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        reg_username = data["reg_name"]
        reg_password = data["reg_password"]
        g_num = data["g_num"]
        web_pin = data["web_pin"]

        if Student.query.filter_by(username=reg_username).first() or Student.query.filter_by(g_num=g_num).first():
            flash("Username / G-Num account already in the Database. Try again",  "error")

        elif valid_works(reg_username, reg_password):
            if valid_web(g_num, web_pin):
                password = cipher.encrypt(reg_password.encode())
                new_user = Student(username=reg_username, password=password)
                db.session.add(new_user)
                login_user(new_user)
                g_num = cipher.encrypt(g_num.encode())
                web_pin = cipher.encrypt(web_pin.encode())
                db.session.query(Student).filter_by(username=current_user.username).update(
                        {'g_num': g_num, 'web_pin': web_pin}
                        )
                db.session.commit()
                return redirect(url_for("dashboard"))
            flash("Banner web login details are not accurate, try again",  "error")
        else:
            flash("Degree Works is inaccurate, try again",  "error")

    return render_template("index.html", login=False)

@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    if current_user:
        if request.method == "POST":
            return redirect(url_for("choice"))

        degree_info = get_degree_info(current_user.username, cipher.decrypt(current_user.password).decode())
        if degree_info.get("error"):
            flash(degree_info["error"], "error")
            return url_for(homepage)
        else:
            session["remaining"] = get_remaining(degree_info["classes_taken"])
            session["requested"]=[]
            session["index"]=0
            subject_info = taken_info(degree_info["classes_taken"])
            return render_template("reg_page.html", subject_info=subject_info)
    else:
        return redirect(url_for('logout'))

@app.route("/choice", methods=["GET", "POST"])
@login_required
def choice():
    if session:
        if request.method == "POST":
            subject = request.form["selectedValue"]
            session["index"] += 1
            if session["index"] > 7 or subject == 'Next':
                return f"{session['requested']}"
            session["requested"].append(subject)
            session["remaining"].remove(subject)
            session.modified = True
        return render_template("a.html", remaining=session["remaining"])
    else:
        return redirect(url_for('logout'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)