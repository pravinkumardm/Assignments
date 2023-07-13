from flask import Flask, render_template, request, redirect
import string
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def form_report():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Save data to database
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
            return render_template('report.html', test_status = "Pass")
        else:
            return render_template('report.html', test_status= "Fail", failure_result=text_status)


def runcheck(password):
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
    status.append(password[-1] in string.digits)
    return status
    # check number at last position


if __name__ == "__main__":
    app.run(debug=True)
