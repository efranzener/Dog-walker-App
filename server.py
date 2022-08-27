from http import server
from flask import (Flask, render_template, request, flash, session, redirect, url_for, logging, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from sqlalchemy.sql import exists

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
            flash(f"Welcome, {user.fname}!")
            
            return redirect(url_for("user_dashboard", user_id=user_id, fname=user.fname))

    else:
        return redirect(url_for("homepage"))


@app.route('/user_dashboard/<user_id>', methods=["GET", "POST"])
def user_dashboard(user_id):
    """ finish account as a sitter or pet_owner or redirect to user"""

    user = crud.get_user_by_id(user_id)

    if user.pet_owner != None:
        pet_owner = crud.get_petowner_by_user_id(user_id)
    else:
        flash("You need to create a pet owner profile before being able to add your pets")
        redirect('/homepage')

    if request.method == "GET":
        
        return render_template("user_dashboard.html", pet_owner = pet_owner, user = user)
    
    elif request.method == "POST":
        
        user_type = request.form.get('account_type')
        print(f"my email is {session['user_email']}")
       
        if "finished" in user_type:
            
            return redirect(url_for("user_dashboard", user = user))
        elif "sitter" in user_type:

            return redirect(url_for("sitter_signup", user_id = user.user_id))

        elif "pet_owner" in user_type:

            return redirect(url_for("petowner_signup", user_id = user.user_id))
       
    
    
    return redirect(url_for("user_dashboard", user = user))
    

@app.route("/sitter_signup/<user_id>", methods=["GET", "POST"])
def sitter_signup(user_id) :     
    
    user = crud.get_user_by_id(user_id)
    
    if request.method == "GET":
        if crud.sitter_exists(user_id) == True:
            flash("You already created your sitter profile")  

            return redirect(url_for("user_dashboard", user_id = user_id))
        
        else:
            return render_template("sitter_signup.html", email = user.email, fname = user.fname, user_id = user_id)  

    else:    
        email = session["user_email"]
        user = crud.get_user_by_email (email)
        user_id = user.user_id

        years_of_experience = request.form.get("years_of_experience")
        summary = request.form.get("summary")
        rate = request.form.get("rate")

        sitter = crud.create_sitter( user_id = user_id, years_of_experience = years_of_experience, summary = summary, rate = rate)
        db.session.add(sitter)
        db.session.commit()
        
        flash("Sitter profile sucessfully completed!", "sucess")
        return redirect(url_for("user_dashboard", user_id = user_id))

        # return redirect(url_for("show_user_profile", user_id = user_id, fname = user.fname))
    

@app.route("/petowner_signup/<user_id>", methods=["GET","POST"])
def petowner_signup(user_id):
    """ create a new pet owner"""
   
    if request.method == "GET":
        user = crud.get_user_by_id(user_id)
        
        if crud.petowner_exists(user_id) == True:
            flash("You already created your pet_owner profile")
              
            return redirect(url_for("user_dashboard", user_id = user_id))

        return render_template("petowner_signup.html", email = user.email, fname = user.fname, user_id = user_id)
    else:
        user = crud.get_user_by_id(user_id)        
        email = session["user_email"]
        user_id = user.user_id
        num_pets = request.form.get("num_pets")
        pet_owner = crud.create_pet_owner( user_id = user_id, num_pets = num_pets)
        
        db.session.add(pet_owner)
        db.session.commit()
        flash("Profile sucessfully completed! Proceed to add your dog info.")
                
        return redirect(url_for("create_pet_profile", num_pets=num_pets, user = user, user_id =user.user_id, pet_owner = pet_owner))


@app.route("/add_dog/<user_id>", methods=["GET", "POST"])
def create_pet_profile(user_id):
    
    # if 'email' in session:
    user = crud.get_user_by_id(user_id)
    pet_owner = crud.get_petowner_by_user_id(user_id)
    fname = user.fname
    num_pets = pet_owner.num_pets
    pet_owner_id = pet_owner.id
    pets_registered = crud.get_pets_by_ownerid(pet_owner_id)
    total_pets = crud.get_total_pets_by_owner(pet_owner_id)
    print(f"number of pets registered{pets_registered}")
    
    while total_pets < num_pets:
                  
        if request.method == "GET":
            return render_template("add_dog.html", total_pets = total_pets, fname =fname,  pets_registered = pets_registered, num_pets = num_pets, user = user, user_id = user.user_id, pet_owner=pet_owner)
        
        elif request.method == "POST":
            
            name = request.form.get("name")
            breed = request.form.get("breed")
            age = request.form.get("age")
            size = request.form.get("size")
            allergies = bool(request.form["allergies"])
            allergies_kind = request.form.get("kind_allergies")
            house_trained = bool(request.form["hstrained"])
            friendly_w_dogs = bool(request.form["dog_friendly"])
            friendly_w_kids = bool(request.form["kid_friendly"])
            spayed_neutered = bool(request.form["spayed_neutered"])
            microchipped = bool(request.form["microchipped"])
            additional_info = request.form.get("additional_info")
            emergency_contact_name = request.form.get("emergency_contact")
            emergency_contact_relationship = request.form.get("emergency_relationship")
            emergency_phone = request.form.get("emergency_phone")
            profile_pic = request.form.get("profile_pic")

            
            pet = crud.create_pet(name= name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, house_trained=house_trained, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, additional_info=additional_info, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owner_id=pet_owner.id)
            db.session.add(pet)
            db.session.commit()
            flash("Pet sucessfully added!") 
            
        total_pets += 1       
        return render_template("add_dog.html", total_pets = total_pets, fname = fname, pets_registered = pets_registered, num_pets = num_pets, user = user, user_id = user_id, pet_owner=pet_owner)
    
    flash(f"You already added the amount the same amount od dogs informed in your profile, soon you will be able to edit yours and your dogs profiles")
    return redirect(url_for("user_dashboard", user = user, user_id = user_id))
    
    
@app.route("/new_booking/<user_id>", methods = ["GET"])
def get_booking_form(user_id):
    """get booking form"""
            
    if "user_email" not in session:
        return redirect('/')
    
    
    email = session.get('user_email')
    user = crud.get_user_by_email(email)
    sitters = crud.get_all_other_sitters(user_id)
    pet_owner = crud.get_petowner_by_user_id(user_id)
    pet_owner_id = pet_owner.id
    pets = crud.get_pets_by_ownerid(pet_owner_id)
    
    return render_template("new_booking.html", pet_owner = pet_owner, sitters = sitters, user_id = user_id, pets = pets)    
    
    
@app.route("/create_booking/<pet_owner_id>", methods=["POST"])
def create_booking(pet_owner_id):
    """ create a new booking"""
    
    if "user_email" not in session:
        return redirect('/')
    
    email = session.get('user_email')
    user = crud.get_user_by_email(email)
    # pet_owner = crud.get_petowner_by_id(pet_owner_id)
    # sitters = crud.get_sitters()
    

    pet_owner_id = pet_owner_id
    sitter_id = request.form.get("sitter_id")
    pet_id = request.form.get("pet_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")   
    weekly = bool(request.form["weekly"])
    
    
    print(f" my sitter id is {sitter_id}")
    print(f" my pet id is {pet_id}")
    booking = crud.create_booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, weekly=weekly)
    
    flash("booking sucessfully created")
    
    # if weekly:
    #     crud.
        
    
    return redirect(url_for("user_dashboard", user_id = user.user_id))


@app.route("/user_profile/<user_id>", methods=["GET", "POST"])
def show_user_profile(user_id):
    """Show the user profile for that user."""
    
    if request.method == "GET":
        # user = crud.get_user_by_id(user_id)
            
    return render_template("user_profile_page.html", user_id=user_id, )


@app.route('/forgot_password', methods=["GET"])
def forgotPassword():
    """render forgot my password page"""

    return render_template("forgot_password.html")
        
  
@app.route('/sitters')
def all_sitters():
    """View all sitters in db"""
    
    sitters = crud.get_sitters()
   
    return render_template("all_sitters.html", sitters=sitters)


@app.route('/sitters/<user_id>')
def get_sitter(user_id):
    """View all sitters in db"""
    
    sitter = crud.get_sitter_by_user_id(user_id)
    
    return render_template("/")


@app.route("/all_my_dogs/<user_id>")
def show_all_dogs(user_id):
    """return all the dogs under a specific pet_id"""

    if crud.petowner_exists(user_id) != True:
        flash("You need to create your pet_owner profile to be able to add and see your dogs.")

        return redirect(url_for("petowner_signup", user_id = user_id))

    else:
        user = crud.get_user_by_id(user_id)
        pet_owner = crud.get_petowner_by_user_id(user_id)
        pet_owner_id = pet_owner.id
        my_pets = crud.get_pets_by_ownerid(pet_owner_id)
        
        if my_pets == 0:
            total_pets = 0

            return render_template("add_dog.html", user = user, pet_owner = pet_owner, total_pets = total_pets, pet_owner_id = pet_owner_id )
        else:

            return render_template("all_my_dogs.html", my_pets = my_pets, pet_owner_id = pet_owner_id)

        

@app.route("/bookings/<pet_owner_id>")
def get_all_bookings(pet_owner_id):
    """Return all the bookings made by a specific pet owner"""
    
    my_bookings = crud.get_bookings_by_pet_owner(pet_owner_id)
    
    return render_template("all_bookings.html", my_bookings = my_bookings)


# @app.route("/logout")
# def logout():
#    """remove the username from the session if it is there"""
   
#    session.pop('user', None)
#    return redirect(url_for('homepage'))



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

