from http import server
from flask import (Flask, render_template, request, flash, session, redirect, url_for, logging)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.secret_key = "Mys3cr3tk3y"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Display the homepage"""
  
    return render_template('homepage.html')

    return 

@app.route('/sign_up', methods=["GET", "POST"])
def create_account():
    """create an account"""
    """redirect to sitter or pet signup form, depending on the users choice"""

    fname = request.form.get("fname")
    lname= request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    mobile = request.form.get("mobile")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    account_type = request.form.get("account_type")
    print (f"this is {account_type}")


    sitter = crud.get_sitter_by_email(email)
    pet_owner = crud.get_pet_owner_by_email(email)
    if sitter:
        flash("Cannot create an account with that email. Please try again.")
    
    elif pet_owner:
        flash("Cannot create an account with that email. Please try again.")

    else:
        if request.method == "POST":
            flash("POst:", request.form)
            if "sitter" in account_type:
                
                return render_template("sitter-signup.html", fname=fname, lname=lname, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code)
            
            elif "dog_owner" in account_type:

                return render_template("petownersignup.html", fname=fname, lname=lname, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code)
        else:
            return render_template("signup.html")
    flash("oops")
    return render_template("signup.html")

@app.route('/sitter-signup', methods=["GET", "POST"])
def sitter_signup():
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
    profile_pic = "profile picture"
    years_of_experience = request.form.get("years_of_experience")
    summary = request.form.get("summary")
    rate = request.form.get("rate")


    sitter = crud.get_sitter_by_email(email)
    if sitter:
        print("Cannot create an account with that email. Please try again.")
    if request.method == "POST":
        sitter = crud.create_sitter(fname=fname, lname=lname, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic, years_of_experience=years_of_experience, summary=summary, rate=rate)
        db.session.add(sitter)
        db.session.commit()
        print("Account sucessfully created! Please log in.")
        return redirect(url_for("homepage"))
    elif request.method == "GET":
        return render_template("sitter-signup.html")

    return redirect("homepage.html")
    

@app.route('/petowner-signup', methods=["GET","POST"])
def owner_signup():
    """ create a new pet owner"""
   
    # fname = request.form.get("fname")
    # lname = request.form.get("lname")
    # email = request.form.get("email")
    # password = request.form.get("password")
    # mobile = request.form.get("mobile")
    # address = request.form.get("address")
    # city = request.form.get("city")
    # state = request.form.get("state")
    # zip_code = request.form.get("zip_code")
    profile_pic = request.form.get("profile_pic")
    num_pets = request.form.get("num_pets")
    

    # pet_owner = crud.get_pet_owner_by_email(email)
    # if pet_owner:
    #     flash("Cannot create an account with that email. Please try again.")
    # else:
    pet_owner = crud.create_pet_owner(fname=fname, lname=lname, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic, num_pets=num_pets)
    db.session.add(pet_owner)
    db.session.commit()
    flash("Account sucessfully created! Please log in.")


    return redirect("templates/homepage.html")



@app.route('/login', methods=["GET","POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")

    sitter = crud.get_sitter_by_email(email)
    pet_owner = crud.get_pet_owner_by_email(email)

    if sitter and sitter.password == password:
        print(f"logging in sitter {email}")
        return render_template("sitter_dashboard.html")

    # if not sitter or sitter.password != password:
    #     if not pet_owner or pet_owner.password != password:
    #         flash("Something went wrong. Please check your email and password and try again")

    # elif sitter and sitter.password == password:
    #     session["sitter_email"] = sitter.email
    #     flash(f"Welcome, {sitter.email}!")

    #     return redirect("sitter_dashboard.html")

    # elif pet_owner and pet_owner.password == password:

    #     # Log in pet_owner by storing their email in session

    #     session["pet_owner"] = pet_owner.email
    #     flash(f"Welcome, {pet_owner.email}!")

    #     return redirect("pet_owner_dashboard.html")

    return redirect("/")


@app.route('/forgot-password', methods=["GET", "POST"])
def forgotPassword():
    """render forgot my password page"""

    return render_template("forgot-password.html")
        
        
  

@app.route('/sitters')
def all_sitters():
    """View all sitters in db"""
    
    sitters = crud.get_sitters()

    return render_template("all_sitters.html", sitters=sitters)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

