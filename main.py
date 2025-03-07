from flask import request, render_template, Flask, url_for, redirect, session, flash, jsonify
from validity import valid_web, valid_works
from courses import get_degree_info
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from timetables import retrieve_classes_website, clash, convert_time, add_classes, add_crns
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
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@login.user_loader
def load_user(user):
    return Student.query.get(user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))


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
            return render_template('index.html',login=True, redirect_target=url_for("dashboard"))
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
    
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if session:
        if not session.get("remaining", None):
            session["degree_info"] = get_degree_info(current_user.username, cipher.decrypt(current_user.password).decode())
            if session["degree_info"].get("error"):
                flash(session["degree_info"]["error"], "error")
                return url_for(homepage)
            else:
                session["remaining"] = get_remaining(session["degree_info"]["classes_taken"])  
            session["available_courses"] = retrieve_classes_website(session["remaining"])
            session["schedule"]={}
            
        return render_template("dashboard.html", subjects = session["available_courses"], schedule= session["schedule"])
    
    else:
        return redirect(url_for('logout'))


@app.route('/profile')
def profile():
    return render_template('profile.html')   

    
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
    
@app.route('/submit', methods=['POST'])
def submit():
    print(session["degree_info"])
    subject = request.form.get('subject')
    crn = request.form.get('crn')
    days = request.form.get('days')
    time = request.form.get('timeSel')
    converted_time= convert_time(time)   

    #check if max amount of classes reached
    if len(session["schedule"]) == 7:
        flash("Maximum amout of classes(7) added")
        return redirect(url_for('dashboard'))
    
    #check for clash
    clashes = clash(session["schedule"], crn, subject, days, converted_time)
    if not clashes[0] :
        session["schedule"][crn] = {"subject": subject, "days":days, "time": time, "converted_time":converted_time}
        flash(clashes[1], "success")  
        return redirect(url_for('dashboard'))
    
    flash(clashes[1])
    return redirect(url_for('dashboard'))


@login_required 
@app.route('/added')
def added():
    #shows the current schedule on the webpage
    return jsonify(session["schedule"])


@app.route('/randomizer', methods=['POST'])
def submit_class_count():
    class_count = int(request.form.get('classCount'))
    classes_added = add_classes(session["available_courses"], session["schedule"], class_count)
    flash(f"{classes_added} classes added")
    if class_count !=classes_added:
        flash(f"Only a maximum of 7 classses may be added")
    return redirect(url_for("dashboard"))

@app.route('/delete', methods=['POST'])
def delete_course():
    crn = request.form.get('crn')
    print(crn)
    if session:
        if session.get("schedule") and session["schedule"].get(crn):
            session["schedule"].pop(crn)
            session.modified = True
            flash("Subject successfully removed")
            return redirect(url_for('dashboard'))
        flash("Error in deleting the requested CRN, try again")
        return redirect(url_for('dashboard'))

@app.route('/final_submission', methods=["POST"])
def final_submission():
    chosen_courses=[]
    for crn in session["schedule"]:
        chosen_courses.append(crn)
    add_crns(cipher.decrypt(current_user.g_num).decode(), cipher.decrypt(current_user.web_pin).decode(), chosen_courses)
    flash("Successful")
    return redirect(url_for('dashboard'))
        

if __name__ == "__main__":
    app.run(debug=True, port=5001)