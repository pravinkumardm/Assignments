from flask import Flask, render_template, request, redirect, session
import string
from database.database import *
app = Flask(__name__)
app.secret_key = 'My_Random_Secret_Key_abvasldugjklsda12348@#$%'


@app.route('/')
def index():
    '''
    Function to render the default page, creates a session if it does not exist to count the consecutive fails
    '''
    if 'fail_count' not in session:
        session['fail_count'] = 0
    return render_template('index.html')


@app.route('/report', methods=['POST'])
def form_report():
    '''
    Function to render the report page, gets called on click of "Submit" in the form
    '''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        insert_password(username, password)
        check_result = runcheck(password)
        text_status = []
        for k,v in enumerate(check_result):
            if k==0 and not v:
                text_status.append("You did not use an uppercase character in your password")
            elif k==1 and not v:
                text_status.append("You did not use a lowercase character in your password")
            elif k==2 and not v:
                text_status.append("You did not use a number at the end of your password")
        print(text_status)
        if all(check_result):
            session['fail_count'] = 0
            return render_template('report.html', test_status = "Pass")
        else:
            session['fail_count'] += 1
            return render_template('report.html', test_status= "Fail", failure_result=text_status, failcount=session['fail_count'])


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
    app.run(debug=False)
