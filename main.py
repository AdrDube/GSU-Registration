from flask import request, render_template, Flask, url_for, redirect, session
from validity import valid_web, valid_works
from courses import get_transcripts
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from dotenv import dotenv_values
from mySQL import taken_info, get_remaining
from cryptography.fernet import Fernet

app = Flask("My app")
secrets = dotenv_values(".env")

cipher = Fernet(secrets["cipher"].encode())

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


@login.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = data["password"]
        user = Student.query.filter_by(username=username).first()
        if user and password == cipher.decrypt(user.password).decode():
            login_user(user)
            return redirect(url_for("homepage"))
        return redirect(url_for("invalid_login"))
    return render_template("login.html", login_text="Login")

@app.route("/invalid_login", methods=["GET", "POST"])
def invalid_login():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = data["password"]
        user = Student.query.filter_by(username=username).first()
        if user and password == cipher.decrypt(user.password).decode():
            login_user(user)
            return redirect(url_for("homepage"))
    return render_template("login.html", login_text="Invalid Login, please try again")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        reg_username = data["reg_name"]
        reg_password = data["password"]

        if Student.query.filter_by(username=reg_username).first():
            return redirect(url_for("in_dbs"))

        if valid_works(reg_username, reg_password):
            password = cipher.encrypt(reg_password.encode())
            new_user = Student(username=reg_username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("web"))
        return redirect(url_for("invalid_works"))
    return render_template("works.html")

@app.route("/invalid_works", methods=["GET", "POST"])
def invalid_works():
    if request.method == "POST":
        data = request.form
        reg_username = data["reg_name"]
        reg_password = data["password"]
        if Student.query.filter_by(username=reg_username).first():
            return redirect(url_for("in_dbs"))
        if valid_works(reg_username, reg_password):
            password = cipher.encrypt(reg_password.encode())
            new_user = Student(username=reg_username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("web"))
    return render_template("invalid_works.html")

@app.route("/web", methods=["GET", "POST"])
@login_required
def web():
    if request.method == "POST":
        data = request.form
        g_num = data["g_num"]
        web_pin = data["web_pin"]
        if valid_web(g_num, web_pin):
            g_num = cipher.encrypt(g_num.encode())
            web_pin = cipher.encrypt(web_pin.encode())
            db.session.query(Student).filter_by(username=session['username']).update(
                        {'g_num': g_num, 'web_pin': web_pin}
                        )
            db.session.commit()       
            return redirect(url_for("homepage"))
        return render_template("invalid_web.html")
    return render_template("web.html")

@app.route("/invalid_web", methods=["GET", "POST"])
@login_required
def invalid_web():
    if request.method == "POST":
        data = request.form
        g_num = data["g_num"]
        web_pin = data["web_pin"]
        if valid_web(g_num, web_pin):
            g_num = cipher.encrypt(g_num.encode())
            web_pin = cipher.encrypt(web_pin.encode())
            db.session.query(Student).filter_by(username=session['username']).update(
                {'g_num': g_num, 'web_pin': web_pin}
            )
            db.session.commit()
            return redirect(url_for("homepage"))
    return render_template("/invalid_web.html")

@app.route("/contained", methods=["GET", "POST"])
def in_dbs():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = data["password"]
        user = Student.query.filter_by(username=username).first()
        if user and password == cipher.decrypt(user.password).decode():
            db.session.add(user)
            login_user(user)
            return redirect(url_for("homepage"))
        return redirect(url_for("invalid_login"))
    return render_template("login.html", login_text="User and password already in database. Login")

@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    if request.method == "POST":
        return redirect(url_for("choice"))
    subjects = get_transcripts(current_user.username, cipher.decrypt(current_user.password).decode())
    subject_info = taken_info(subjects)
    session["remaining"] = get_remaining(subjects)
    session["requested"]=[]
    session["index"]=0
    return render_template("reg_page.html", subject_info=subject_info)

@app.route("/choice", methods=["GET", "POST"])
@login_required
def choice():
    if request.method == "POST":
        subject = request.form["selectedValue"]
        session["index"] += 1
        if session["index"] > 7 or subject == 'Next':
            return f"{session['requested']}"
        session["requested"].append(subject)
        session["remaining"].remove(subject)
        session.modified = True
    return render_template("a.html", remaining=session["remaining"])

if __name__ == "__main__":
    app.run(debug=True, port=5001)