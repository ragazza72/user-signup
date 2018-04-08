from flask import Flask, request, redirect, render_template
import os
import jinja2
import cgi
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)




@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()
   
@app.route("/welcome", methods=['POST', 'GET'])
def welcome():
    user_name = request.form['Username']
    password1 = request.form['Password']
    password2 = request.form["password2"]
    email = request.form['email']

    username_err_msg = ""
    password_err_msg = ""
    password_match_error = ""
    email_error_msge = ""
    error = False

    if is_input_not_valid(user_name):
        username_err_msg = "This is not a valid username"
        error = True

    if is_input_not_valid(password1):
        password_err_msg = "This is an not a valid password"
        error = True 

    if not_matching_passwords(password1, password2):
        password_match_error = "Your passwords do not match"
        error = True

    if email_not_valid(email):
        email_error_msge = "This is not a valid email"
        error = True

    if error:
        return render_template("index.html",
            username=username_err_msg,
            password=password_err_msg,
            password_again=password_match_error,
            email_error=email_error_msge
        )

    template = jinja_env.get_template('welcome_page.html')
    return template.render(name=user_name)

@app.route("/signup")
def signup():
    template = jinja_env.get_template('index.html')  
    return template.render()     

def is_input_not_valid(input):
    if input == "" or len(input) < 3 or len(input) > 20 or " " in input:
        return True
    return False

def not_matching_passwords(password1, password2):
    if not password1 == password2:
        return True
    return False

def email_not_valid(email):
    if not email == '':
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email) or len(email) < 3 or len(email) > 20:
            return True 
    return False 


app.run()