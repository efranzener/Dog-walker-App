from http import server
from flask import (Flask, render_template, request, flash, session, redirect, url_for, logging, jsonify)
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

    

@app.route('/signup', methods=["GET", "POST"])
def create_account():
    """create an account"""

    if request.method == "GET":
        return render_template("signup.html")
    else:

        fname = request.form.get("fname")
        lname= request.form.get("lname")
        dob = request.form.get("dob")
        email = request.form.get("email")
        password = request.form.get("password")
        mobile = request.form.get("mobile")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip_code")
        profile_pic = request.form.get("profile_pic")
    

        user = crud.get_user_by_email(email)
        if user:
            flash("Cannot create an account with that email. Please try again.", "error")
            return  redirect("/")
        
        else:
            user = crud.create_user(fname=fname, lname=lname, dob=dob, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic)
            db.session.add(user)
            db.session.commit()
            flash("Account sucessfully created! Please login.", "sucess")
            return redirect(url_for("homepage"))



@app.route('/login', methods=["GET","POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    
    
    if request.method == "POST":
        if not user or user.password != password:
            flash("Something went wrong. Please check your email and password and try again")
            return redirect(url_for("homepage"))
        elif user and user.password == password:
            
            user_id = user.user_id
            session["user_email"] = user.email
            print(session['user_email'])
            print(f"my session is{session}")
            print(f"******************************{user_id}")
            
            flash(f"Welcome, {user.fname}!")
            # return redirect("/user_dashboard/{user_id}", user_id=user_id, fname=user.fname)
            return redirect(url_for("user_dashboard", user_id=user_id, fname=user.fname))
        # else:
        #     return redirect(url_for("homepage"))
    else:
        return redirect(url_for("homepage"))


@app.route('/user_dashboard/<user_id>', methods=["GET", "POST"])
def user_dashboard(user_id):
    """ finish account as a sitter or pet_owner"""
    
    print(f"user_dashboard user_id: {user_id}")
    
    # sitter = crud.get_sitter_by_id()
    # print(f"I'm a sitter and my id is {sitter.id} line 93")
    # user = crud.get_user_by_id(user_id)
    
    if request.method == "GET":
        user = crud.get_user_by_id(user_id)
        print(f"i am {user_id}")
        return render_template("user_dashboard.html", user_id=user_id, fname=user.fname)
    
    elif request.method == "POST":
        
        user_type = request.form.get('account_type')

        # print(f"account type is:{user_type} {user_id}")
       
        email = session["user_email"]
        # user = crud.get_user_by_id(user_id)
        # print(f"im line 101 {email} {user_id}")
        if "sitter" in user_type:
            # print(f"i'm line 113 {user_id}")
            return redirect(url_for("sitter_signup", user_id = user_id))

        elif "pet_owner" in user_type:
            return redirect(url_for("petowner_signup", user_id = user.user_id))
        # else:
        #     redirect(url_for("user_dashboard", user=user))
    
    
    return redirect(url_for("process_login"))
    

@app.route("/sitter_signup/<user_id>", methods=["GET", "POST"])
def sitter_signup(user_id) :       
    
    # print(f"sitter sign up{user_id}")
    if request.method == "GET":
        
        user = crud.get_user_by_id(user_id)
        # print(f"im user at 127 line {user.user_id}")
        return render_template("sitter_signup.html", email = user.email, fname = user.fname, user_id = user_id)
    else:
        
        print(f"I'm line 136, {user_id}")
        email = session["user_email"]
        user = crud.get_user_by_email (email)
        user_id = user.user_id
        print(f"I'm line 133, email={email} *********** user_id={user_id}**********************************")
        years_of_experience = request.form.get("years_of_experience")
        summary = request.form.get("summary")
        rate = request.form.get("rate")

        sitter = crud.create_sitter( user_id = user_id, years_of_experience = years_of_experience, summary = summary, rate = rate)
        db.session.add(sitter)
        db.session.commit()
        flash("Account sucessfully created!", "sucess")
        # user = crud.get_user_by_email(email)
        return redirect(url_for("show_user_profile", user_id = user_id, fname = user.fname))
    

    
@app.route("/user_profile/<user_id>", methods=["GET", "POST"])
def show_user_profile(user_id):
    """Show the user profile for that user."""
    
    if request.method == "GET":
        # user = crud.get_user_by_id(user_id)
        
        print(f'Line 161, Profile page for user: {user_id}')
    
    return render_template("user_profile_page.html", user_id=user_id, )
    

@app.route('/petowner_signup', methods=["GET","POST"])
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



@app.route('/forgot_password', methods=["GET"])
def forgotPassword():
    """render forgot my password page"""

    return render_template("forgot_password.html")
        
        
  

@app.route('/sitters')
def all_sitters():
    """View all sitters in db"""
    
    sitters = crud.get_sitters()

    return render_template("all_sitters.html", sitters=sitters)

@app.route('/logout')
def logout():
   """# remove the username from the session if it is there"""
   
   session.pop('user', None)
   return redirect(url_for('homepage'))



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

