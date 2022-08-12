from http import server
from flask import (Flask, render_template, request, flash, session, redirect, url_for, logging)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "Mys3cr3tk3y"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Display the homepage"""
    
    return render_template('homepage.html')

@app.route("/sitter-signup")
def get_signup_form():
    """display sign up form"""

    return render_template('sitter-signup.html')


@app.route('/signup', methods=["POST"])
def signup():
    """ create a new sitter"""

    fname = request.form.get("fname")
    lname= request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    mobile = request.form.get("mobile")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    profile_pic = request.form.get("profile_pic")
    years_of_experience = request.form.get("years_of_experience")
    summary = request.form.get("summary")
    rate = request.form.get("rate")


    sitter = crud.get_sitter_by_email(email)
    if sitter:
        flash("Cannot create an account with that email. Please try again.")
    else:
        sitter = crud.create_sitter(fname=fname, lname=lname, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic, years_of_experience=years_of_experience, summary=summary, rate=rate)
        db.session.add(sitter)
        db.session.commit()
        flash("Account sucessfully created! Please log in.")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    sitter = crud.get_sitter_by_email(email)
    pet_owner = crud.get_pet_owner_by_email(email)
    if not sitter  or sitter.password != password:
        flash("Something went wrong. Please check your email and password and try again")
    else:
        # Log in user by storing the user's email in session
        session["sitter_email"] = sitter.email
        flash(f"Welcome back, {sitter.email}!")

    return redirect("/")
  

@app.route('/sitters')
def all_sitters():
    """View all sitters in db"""
    
    sitters = crud.get_sitters()

    return render_template("all_sitters.html", sitters=sitters)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

