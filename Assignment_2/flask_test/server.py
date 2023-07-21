from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, Response
from database.database import *
from flask_sqlalchemy import SQLAlchemy
import pymysql, string


app = Flask(__name__)
app.secret_key = 'My_NEW_aldsfyasdifh_Random_Secret_Key_abvasldugjklsda12348@#$%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python_password_checker:DB2023#pythonuser_+@localhost/passwordchecker'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(60), nullable = False)
    lname = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    password = db.Column(db.String(60), nullable = False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    '''
    Function to render the default page, creates a session if it does not exist to count the consecutive fails
    '''

    return render_template('index.html', current_page="home")


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email, password = password).first()
        if user:
            return render_template('SecretPage.html', current_page = "other")
        else:
            return render_template('index.html', message="No Account or Incorrect Details", current_page="home")


@app.route('/signup', methods=["POST", 'GET'])
def signup_page():
    print(request.method)
    if request.method == "GET":
        if 'fail_count' not in session:
            session['fail_count'] = 0
        return render_template("signup.html", failcount = session['fail_count'], current_page="signup")
    if request.method == "POST":
        print("Working")      
        print(request.form)
        fname = request.form['fname']
        lname = request.form['lname']
        Email = request.form['email']
        password = request.form['password']
        if check_email(Email):
            return render_template("index.html", message="Email already exists", current_page="home")
        else:
            check_result = runcheck(password)
            text_status = []
            for k,v in enumerate(check_result):
                if k == 0 and not v:
                    text_status.append("You did not use an uppercase character in your password")
                elif k==1 and not v:
                    text_status.append("You did not use a lowercase character in your password")
                elif k==2 and not v:
                    text_status.append("You did not use a number at the end of your password")
            if all(check_result):
                session['fail_count'] = 0
                new_user = User(fname=fname, lname=lname, email = Email, password = password)
                db.session.add(new_user)
                db.session.commit()
                return render_template('Thankyou.html', message="Thank you for registering!", test_status = "Pass", current_page = "other")
            else:
                session['fail_count'] += 1
                return render_template("signup.html", test_status = "Fail", failure_result = text_status, failcount = session['fail_count'], current_page="signup")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def check_email(Email):
    user = User.query.filter_by(email = Email).first()
    if user:
        return True
    else:
        return False
    

def runcheck(password):
    '''
    Function to check the logic for password checking.
    '''
    status = []
    upper_checker = []
    lower_checker = []
    # check any word is upper case or lower case
    for letter in password:
        if letter in string.ascii_uppercase:
            upper_checker.append(True)
        else:
            upper_checker.append(False)
        if letter in string.ascii_lowercase:
            lower_checker.append(True)
        else:
            lower_checker.append(False)
    status.append(any(upper_checker))
    status.append(any(lower_checker))
    # check number at last position and append to status
    status.append(password[-1] in string.digits)
    return status


if __name__ == "__main__":
    app.run(debug=True)
