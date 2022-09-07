

from __future__ import print_function

from http import server
from flask import (Flask, render_template, request, flash, session, redirect, url_for, logging, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from sqlalchemy.sql import exists
from datetime import datetime
import requests
from werkzeug.utils import secure_filename
import uuid as uuid
import os

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



import cloudinary
import cloudinary.uploader
import cloudinary.api
# #######
import json

config = cloudinary.config(secure=True)

API_KEY = os.environ['cloudinary_api_key']
API_SECRET = os.environ['api_secret']
CLOUD_NAME = os.environ['cloud_name']



CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'




app = Flask(__name__)
app.secret_key = "Mys3cr3tk3y"
app.jinja_env.undefined = StrictUndefined

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


@app.route('/')
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)
    
    return render_template("homepage.html")






# @app.route('/')
# def homepage():
#     """display the homepage"""
    
    
#     return render_template("homepage.html")



@app.route('/signup')
def get_signup():
    """get user signup form"""

    return render_template("signup.html", states=states)


@app.route('/signup', methods=["POST"])
def create_account():
    """create an account"""
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)
    upload_result = None

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
    profile_file = request.files['profilepic']
    profile_name= secure_filename(profile_file.filename)
        
    # set UUID
    profile_pic = str(uuid.uuid1()) + "_" + profile_name
    user = crud.get_user_by_email(email)
    
    
    if user:
        flash("Cannot create an account with that email. Please try again.", "error")    
    else:
        upload_result = cloudinary.uploader.upload(profile_file, public_id=profile_pic)
        user = crud.create_user(fname=fname, lname=lname, dob=dob, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic)
        
        flash("Account sucessfully created! Please login.", "sucess")
        # print(jsonify(upload_result))
        # print(f"Im profile_file {profile_file}, Im profile pic {profile_pic}")
        # print(profile_pic)

        # return (jsonify(upload_result))
        return('/')



@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("Something went wrong. Please check your email and password and try again")
        return redirect('/')
    
    elif user and user.password == password:
        user_id = user.user_id
        session["user_email"] = user.email
        flash(f"Welcome, {user.fname}!")
        
        return redirect(url_for("get_user_dashboard", user_id=user_id, fname=user.fname))


@app.route('/user_dashboard/<user_id>')
def get_user_dashboard(user_id):
    """Show user dashboard"""

    user = crud.get_user_by_id(user_id)

    if user.pet_owner != None:
        pet_owner = crud.get_petowner_by_user_id(user_id)
    else:
        flash("Please finish your pet_owner profile")
    
    if user.sitter != None:
        sitter = crud.get_sitter_by_user_id(user_id)
    else:
        flash("Please finish to your sitter profile")

    return render_template("user_dashboard.html", pet_owner = pet_owner, sitter = sitter, user = user)

    

@app.route("/sitter_signup/<user_id>")
def get_sitter_signup(user_id) :     
    """get sitter sign up form"""
    
    
    user = crud.get_user_by_id(user_id)
    
    if crud.sitter_exists(user_id) == True:
        flash("You already created your sitter profile")  

        return redirect(url_for("user_dashboard", user_id = user_id))
    
    else:
            
        return render_template("sitter_signup.html", user=user)  
        
        
@app.route("/sitter_signup/<user_id>", methods=["POST"])
def sitter_signup(user_id):     
    """create a new sitter profile"""
    
    user = crud.get_user_by_id(user_id)
    
    if 'user_email' in session:
      
        user = crud.get_user_by_id(user_id)
        user_id = user.user_id
        
        years_of_experience = request.form.get("experience")
        summary = request.form.get("summary")
        rate = request.form.get("rate")
        
        sitter = crud.create_sitter( user_id = user_id, years_of_experience = years_of_experience, summary = summary, rate = rate)
        
        flash("Sitter profile sucessfully completed!", "success")
        
        return redirect(url_for("get_user_dashboard", user_id = user_id))
    
    return redirect('/')    
  
@app.route("/user_profile/<user_id>")
def get_profile_page(user_id):
    """display user profile page"""


    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(user_id)
            
        if sitter:
            sitter=crud.get_sitter_by_id(user_id)
            
        
        public_id =  user.profile_pic        
        cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        if 'secure_url' in cloud_pic:
            profile_pic = cloud_pic['secure_url']
            
        return render_template("user_profile_page.html",
                           profile_pic=profile_pic, pet_owner = pet_owner, sitter = sitter, user = user)
    else:
        return redirect('/')
    
    
@app.route("/user_profile/<user_id>/update")
def get_profile_update_form(user_id):
    """get profile update form"""

    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        
        public_id =  user.profile_pic        
        cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        if 'secure_url' in cloud_pic:
            profile_pic = cloud_pic['secure_url']
        
        return render_template('update_profile.html',  profile_pic = profile_pic, pet_owner = pet_owner, sitter = sitter, user = user)
    else:
        return redirect('/')
    
    
@app.route("/user_profile/<user_id>/update", methods=['POST'])
def update_user_profile(user_id):
    """ update user profile page """
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)
    upload_result = None
    
    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        
        user.fname = request.form.get("fname")
        user.lname= request.form.get("lname")
        user.dob = request.form.get("dob")
        user.email = request.form.get("email")
        user.password = request.form.get("password")
        user.mobile = request.form.get("mobile")
        user.address = request.form.get("address")
        user.city = request.form.get("city")
        user.state = request.form.get("state")
        user.zip_code = request.form.get("zip_code")
        profile_file = request.files['profilepic']
        profile_name = secure_filename(profile_file.filename)
        
        # set UUID
        user.profile_pic = str(uuid.uuid1()) + "_" + profile_name

        # save new profile pic into claudinary
        upload_result = cloudinary.uploader.upload(profile_file, public_id=user.profile_pic)
        
        db.session.commit()
        flash('Your user information was sucessfully updated')
        
        return redirect(url_for('get_profile_page', user_id = user_id))
    else:
        redirect('/')
    
@app.route("/sitter_profile/<user_id>/update", methods=['POST'])
def update_sitter_profile(user_id):
    """ update sitter_profile_page """
    
    if 'user_email' in session:
        
        email = session["user_email"]
        user = crud.get_user_by_email (email)
        sitter = crud.get_sitter_by_user_id(user_id)

        sitter.years_of_experience = request.form.get("experience")
        sitter.summary = request.form.get("summary")
        sitter.rate = request.form.get("rate") 
        
        db.session.commit()
        
        flash('Your sitter profile was sucessfully updated')
        
    else: 
        redirect('/')
        
    return redirect(url_for('get_profile_page', user_id = user_id))
   

@app.route("/petowner_signup/<user_id>")
def petowner_signup_form(user_id):
    """ get pet owner sign up form """
   
    if 'user_email' in session:
        user = crud.get_user_by_id(user_id)
        
        if crud.petowner_exists(user_id) == True:
                
            return redirect(url_for("update_user_profile", user_id = user_id))
    
        return render_template("petowner_signup.html", user=user)
    
    return('/')


@app.route("/petowner_signup/<user_id>", methods=["POST"])
def petowner_signup(user_id):
    """ create a new pet owner"""
   
   
    user= crud.get_user_by_id(user_id)        
    email = session["user_email"]
    user_id = user.user_id
    num_pets = request.form.get("num_pets")
    
    pet_owner = crud.create_pet_owner( user_id = user_id, num_pets = num_pets)

    flash("Profile sucessfully completed! Proceed to add your dog info.")
            
    return redirect(url_for("create_pet_profile", num_pets=num_pets, user = user, user_id =user.user_id, pet_owner = pet_owner))


@app.route("/petowner_profile/<user_id>/update", methods=['POST'])
def update_petowner_profile(user_id):
    """ update pet owner profile page """
    
    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        pet_owner = crud.get_petowner_by_user_id(user_id)
        pet_owner.num_pets = request.form.get("num_pets")
        
        db.session.commit()
        
        flash("Your pet owner profile was sucessfully updated!")
        return redirect(url_for('get_profile_page', user_id = user_id))
    else: 
        return redirect('/')
    
@app.route("/add_dog/<user_id>", methods=["GET", "POST"])
def create_pet_profile(user_id):
    
    if "user_email" not in session:

        redirect("/")
    else:

        user = crud.get_user_by_id(user_id)
        if crud.petowner_exists(user_id):
            pet_owner = crud.get_petowner_by_user_id(user_id)
            fname = user.fname
            num_pets = pet_owner.num_pets
            pet_owner_id = pet_owner.id
            pets_registered = crud.get_pets_by_ownerid(pet_owner_id)
            total_pets = crud.get_total_pets_by_owner(pet_owner_id)
            print(f"number of pets registered{pets_registered}")
        else:
            flash("Please finish your pet owner profile to be able to add a pet")

            return redirect(url_for("petowner_signup", user_id = user_id))
        
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
                
                flash("Pet sucessfully added!") 
                
            total_pets += 1       
        return redirect(url_for("get_user_dashboard", user_id=user_id))
    
    return redirect(url_for("get_user_dashboard", user_id=user_id))

    
    
@app.route("/create_booking/<user_id>")
def get_booking_form(user_id):
    """get booking form"""
            
    if "user_email" not in session:
        return redirect('/')
    
    else: 
        if crud.petowner_exists(user_id):
            pet_owner = crud.get_petowner_by_user_id(user_id)
            pet_owner_id = pet_owner.id
            email = session['user_email']
            # user = crud.get_user_by_email(email)
            sitters = crud.get_all_other_sitters(user_id)
            pet_owner = crud.get_petowner_by_user_id(user_id)
            pet_owner_id = pet_owner.id
            pets = crud.get_pets_by_ownerid(pet_owner_id)
        else:
            flash("Please finish your pet owner profile to be able to book")

            return redirect(url_for("petowner_signup", user_id = user_id))
        
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
    
    print(f" my start_date is  {start_date}")
    print(f" my end_date is {end_date}")
    print(f" my start_time is {start_time}")
    print(f" my end_time is {end_time}")
    print(f" my sitter id is {sitter_id}")
    print(f" my pet id is {pet_id}")

    starttime_with_date = start_date + "T" + start_time
    print("starttime_with_date: ", starttime_with_date)
    starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")
    print("starttime_datetime: ", starttime_datetime)

    endtime_with_date = start_date + "T" + end_time
    print("endtime_with_date: ", endtime_with_date)
    endtime_datetime = datetime.strptime(endtime_with_date, "%Y-%m-%dT%H:%M")
    print("endtime_datetime: ", endtime_datetime)

    booking = crud.create_booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=end_date, start_time=starttime_datetime, end_time=endtime_datetime, weekly=weekly)
    
    flash("booking sucessfully created")
   
        
    
    return redirect(url_for("user_dashboard", user_id = user.user_id))



@app.route('/forgot_password', methods=["GET"])
def forgotPassword():
    """render forgot my password page"""

    return render_template("forgot_password.html")
        
  
@app.route('/sitters/<user_id>')
def all_sitters(user_id):
    """View all sitters in db"""
    
    sitters = crud.get_all_other_sitters(user_id)
    
    return render_template("all_sitters.html", sitters=sitters)


@app.route('/sitter_details/<sitter_id>')
def show_sitter_details(sitter_id):
    """Display a specific sitter information, using it's primary key"""
    
    sitter = crud.get_sitter_by_id(sitter_id)
    user = crud.get_user_by_sitter_id(sitter_id)
    
    return render_template("sitter_details.html", sitter = sitter, user = user)


@app.route("/all_my_dogs/<user_id>")
def show_all_dogs(user_id):
    """return all the dogs under a specific pet_id"""

    if crud.petowner_exists(user_id) != True:
        flash("You need to create your pet owner profile to be able to add and see your dogs.")

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

        

@app.route("/my_bookings/<user_id>")
def get_all_bookings(user_id):
    """Return all the bookings made by a specific user"""
    
    sitter_bookings = False
    pet_owner_bookings = False
    if "user_email" not in session: 
    
        redirect("/")
        
    else:
        
        email = session['user_email']
        user = crud.get_user_by_email(email)
        
# check of pet_owner exists to then fetch pet_owner bookings, if  any.
        if crud.petowner_exists(user_id):
            pet_owner_bookings = crud.get_owner_bookings_by_user_id(user_id)

# check of sitter exists to then fetch sitters bookings, if  any.
        if crud.sitter_exists(user_id):
            sitter_bookings = crud.get_sitter_bookings_by_user_id(user_id)

        # if not pet_owner_bookings or sitter_bookings:
        #     flash("Sorry you don't have any bookings yet")
            
        return render_template("all_my_bookings.html", user = user, sitter_bookings = sitter_bookings, pet_owner_bookings = pet_owner_bookings)


@app.route("/logout")
def logout():
    """remove the user from the session if it is there"""
   
    if 'user_email' in session:
        session.pop('user_email', None)
        
    return redirect('/')

# @app.route("/calendar")
# def calendar():
#    """remove the user from the session if it is there"""
   

#    return render_template("calendar_appointment-booking.html")


# #############################################

# # @app.route('users/<user_id>/availability')
# # def get_users_calendar(user_id):
    
# #     calendar = service.calendars().get(calendarId='primary').execute()

# # print calendar['summary']


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
#     
    
#     app.run('localhost', 5000, debug=True)

