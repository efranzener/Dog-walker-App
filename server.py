

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

# import datetime
import os.path

# GOOGLE CALENDAR API IMPORTS
from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# #######
#  CLAUDINARY API IMPORTS
import cloudinary
import cloudinary.uploader
import cloudinary.api
# #######
import json


# Cloudinary API
config = cloudinary.config(secure=True)
API_KEY = os.environ['cloudinary_api_key']
API_SECRET = os.environ['api_secret']
CLOUD_NAME = os.environ['cloud_name']


# Google Calendar API
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'



app = Flask(__name__)
app.secret_key = "Mys3cr3tk3y"
app.jinja_env.undefined = StrictUndefined

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]



@app.route('/')
def homepage():
    """display the homepage"""
    
    
    return render_template("homepage.html")


@app.route('/signup')
def get_signup():
    """get user signup form"""
    
    
    return render_template("signup.html", states=states)


def get_user_consent(user_id):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    user = crud.get_user_by_id(user_id)
    # creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', scopes=SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    # ########################
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_secrets_file=CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = f'http://localhost:5000/user_dashboard/{user_id}'
    authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    login_hint=f'{user.email}',
    prompt='consent',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
    session['state'] = state

    print("Im the authorization url{authorization_url}")
    return(authorization_url)
    # return redirect(url_for("get_user_dashboard", user_id = user.id))


@app.route('/signup', methods=["POST"])
def create_account():
    """create an account"""
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)

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
    
    # return a secure filename ready to be stored
    file_name= secure_filename(profile_file.filename)
        
    # set UUID
    profile_pic = str(uuid.uuid1()) + "_" + file_name
    
    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Please try again.", "danger")    
    else:
        upload_result = cloudinary.uploader.upload(profile_file, public_id=profile_pic)
        user = crud.create_user(fname=fname, lname=lname, dob=dob, email=email, password=password, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic)
        
        flash("Account sucessfully created! Please login.", "sucess")
     
        
    return redirect('/')



@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("Something went wrong. Please check your email and password and try again", "warning")
        return redirect('/')
    
    elif user and user.password == password:
        user_id = user.user_id
        get_user_consent(user_id)
        session["user_email"] = user.email
        flash(f"Welcome, {user.fname}!", "primary")
        
        
        return redirect(url_for("get_user_dashboard", user_id=user_id, fname=user.fname))

# #TESTING
# @app.route('/test')
# def test_api_request():
    
#     if 'credentials' not in session:
#         return redirect('/')

#     # Load credentials from the session.
#     credentials = google.oauth2.credentials.Credentials(session['credentials'])

#     calendar = googleapiclient.discovery.build(
#       API_SERVICE_NAME, API_VERSION, credentials=credentials)

#     # events = drive.files().list().execute()
#     calendar = service.calendars().get(calendarId='testuser.numtwo').execute()

#     print (calendar['summary'])

#     # Save credentials back to session in case access token was refreshed.
#     # ACTION ITEM: In a production app, you likely want to save these
#     #              credentials in a persistent database instead.
#     session['credentials'] = credentials_to_dict(credentials)

#     return jsonify(events)



# ********************
@app.route('/user_dashboard/<user_id>')
def get_user_dashboard(user_id):
    """Show user dashboard"""

    user = crud.get_user_by_id(user_id)
    
    # google calendar id is the first part of the user email. In order to get that, we split the user email using the split() method
    split_email = user.email.split("@")
    
    # create a variable to store the calendar id(splitted email)
    calendar_id = split_email[0]


    return render_template("user_dashboard.html", user = user, calendar_id = calendar_id)

    

@app.route("/sitter_signup/<user_id>")
def get_sitter_signup(user_id) :     
    """get sitter sign up form"""
    
    if 'user_email' in session:
        user = crud.get_user_by_id(user_id)
        
        if crud.sitter_exists(user_id):
            sitter = crud.get_sitter_by_user_id(user_id)
            
            flash("Sitter profile already created. You are welcome to update any information you wish", "success")
            
            return redirect(url_for("get_profile_page", sitter=sitter, user_id=user_id))
        
        else:
                
            return render_template("sitter_signup.html", user = user)  
    
    return('/')    
        
        
@app.route("/sitter_signup/<user_id>", methods=["POST"])
def sitter_signup(user_id):     
    """create a new sitter profile"""
        
    if 'user_email' in session:
      
        user = crud.get_user_by_id(user_id)
        
        years_of_experience = request.form.get("experience")
        summary = request.form.get("summary")
        rate = request.form.get("rate")
        
        sitter = crud.create_sitter(user_id = user_id, years_of_experience = years_of_experience, summary = summary, rate = rate)
        
        flash("Sitter profile sucessfully completed!", "success")
        
        return redirect(url_for("get_user_dashboard", user_id = user_id))
    
    return redirect('/')
    
  
@app.route("/user_profile/<user_id>")
def get_profile_page(user_id):
    """display user profile page"""
    
    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        
        #check if sitter and pet owner are in database
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(user_id)
        if sitter:
            sitter = crud.get_sitter_by_user_id(user_id)
        
        # set cloudinary public_id to current user profile pic 
        public_id =  user.profile_pic
        
        #uses the public id to call cloudinary api to check if current profile picture is uploaded in cloudinary
        try:   
            cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        
        #  if profile pic not uploaded in cloudinary, set profile pic to user.profile_pic (assigned as public id)
        except:
            profile_pic = public_id
        
        # if profile pic in cloudinary, set it to the secure_url, in order to retrive it
        else:
            if 'secure_url' in cloud_pic:
                profile_pic = cloud_pic['secure_url']
        
        return render_template("user_profile_page.html",
                           profile_pic=profile_pic, pet_owner = pet_owner, sitter = sitter, user = user)
    
    return redirect('/')
    
    
@app.route("/user_profile/<user_id>/update")
def get_profile_update_form(user_id):
    """get profile update form"""

    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        
        #check if sitter and pet owner are in database
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(user_id)
            
        if sitter:
            sitter=crud.get_sitter_by_id(user_id)
         
        # set cloudinary public_id to current user profile pic 
        public_id =  user.profile_pic                
        #uses the public id to call cloudinary api to check if current profile picture is uploaded in cloudinary
        try:   
            cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        #  if profile pic not uploaded in cloudinary, set profile pic to user.profile_pic (assigned as public id)
        
        except:
            profile_pic = public_id
        # if
        # profile pic in cloudinary, set it to the secure_url, in order to retrive it
            print("i'm the profile pid line 332", public_id)
        else:
            if 'secure_url' in cloud_pic:
                profile_pic = cloud_pic['secure_url']
                print("im the secure url", cloud_pic['secure_url'])
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
        
        print("I'm the current profile_file", user.profile_pic)

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
        file_name = secure_filename(profile_file.filename)
        print("I'm profile_file", profile_file, file_name)
        
        # set UUID
        user.profile_pic = str(uuid.uuid1()) + "_" + file_name
        db.session.commit()
        
        flash("Your user information was sucessfully updated", "success")
       
        # set cloudinary public_id to current user profile pic 
        public_id =  user.profile_pic        
        
        #uses the public id to call cloudinary api to check if current profile picture is uploaded in cloudinary
        try:   
            cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        #  if profile pic not uploaded in cloudinary, set profile pic to user.profile_pic (assigned as public id)
        except:
            flash("please add a profile_picture")
            user.profile_pic = public_id
        # if profile pic in cloudinary, set it to the secure_url, in order to retrive it
       
        else:
            if 'secure_url' in cloud_pic:
                user.profile_pic = cloud_pic['secure_url']

        # save new profile pic into claudinary
        upload_result = cloudinary.uploader.upload(profile_file, public_id=user.profile_pic)
        
        return redirect(url_for('get_profile_page', user_id = user_id))
    else:
        redirect('/')
    
    
@app.route("/sitter_profile/<user_id>/update", methods=['POST'])
def update_sitter_profile(user_id):
    """ update sitter_profile_page """
    
    if 'user_email' in session:
        
        sitter = crud.get_sitter_by_user_id(user_id)

        sitter.years_of_experience = request.form.get("experience")
        sitter.summary = request.form.get("summary")
        sitter.rate = request.form.get("rate") 
        
        db.session.commit()
        
        flash("Your sitter profile was sucessfully updated!", "success")
        
        return redirect(url_for('get_profile_page', user_id = user_id))
    
    return redirect('/')
        
   
@app.route("/petowner_signup/<user_id>")
def petowner_signup_form(user_id):
    """ get pet owner sign up form """
   
    if 'user_email' in session:
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        user = crud.get_user_by_id(user_id)
        if sitter:
            sitter=crud.get_sitter_by_user_id(user_id)
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(user_id)
            
            flash("Pet owner profile already created. You are welcome to update any information you wish", "info")
            
            return redirect(url_for("get_profile_page", user_id=user_id))
        
        return render_template("petowner_signup.html", user = user)
    
    return redirect('/') 


@app.route("/petowner_signup/<user_id>", methods=["POST"])
def petowner_signup(user_id):
    """ create a new pet owner"""
   
    if 'user_email' in session:
       
        num_pets = request.form.get("num_pets")
        pet_owner = crud.create_pet_owner( user_id = user_id, num_pets = num_pets)

        flash("Profile sucessfully created! Proceed to add your dog info.", "success")
            
        return redirect(url_for("create_pet_profile", user_id = user_id))
    
    return redirect('/')


@app.route("/petowner_profile/<user_id>/update", methods=['POST'])
def update_petowner_profile(user_id):
    """ update pet owner profile page """
    
    if 'user_email' in session:
        
        pet_owner = crud.get_petowner_by_user_id(user_id)
        pet_owner.num_pets = request.form.get("num_pets")
        
        db.session.commit()
        
        flash("Your pet owner profile was sucessfully updated!", "sucess")
        return redirect(url_for('get_profile_page', user_id = user_id))
    
    return redirect('/')
    
    
@app.route("/add_dog/<user_id>", methods=["GET", "POST"])
def create_pet_profile(user_id):
    """create a new dog profile"""
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)
    upload_result = None
    
    user = crud.get_user_by_id(user_id)
    
    if crud.petowner_exists(user_id):
        pet_owner = crud.get_petowner_by_user_id(user_id)
        num_pets = pet_owner.num_pets
        pet_owner_id = pet_owner.id
        pets_registered = crud.get_pets_by_ownerid(pet_owner_id)
        total_pets = crud.get_total_pets_by_owner(pet_owner_id)

    else:
        flash("Please finish your pet owner profile to be able to add a pet", "info")

        return redirect(url_for("petowner_signup", user_id = user_id))
    
    while total_pets != num_pets:
                
        if request.method == "GET":
            return render_template("add_dog.html", total_pets = total_pets, fname = user.fname, pets_registered = pets_registered, num_pets = num_pets, user = user, user_id = user.user_id, pet_owner=pet_owner)
        
        else:
            
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
            profile_file = request.files("profile_pic")
    
            # return a secure filename ready to be stored
            file_name= secure_filename(profile_file.filename)
                
            # set UUID
            profile_pic = str(uuid.uuid1()) + "_" + file_name
            
            if crud.pet_exists(pet_owner_id, name):
    
                flash("pet_already created", "warning")
                return url_for("show_all_dogs", user_id=user_id )
            else:
                upload_result = cloudinary.uploader.upload(profile_file, public_id=profile_pic)
                
                pet = crud.create_pet(name= name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, house_trained=house_trained, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, additional_info=additional_info, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owner_id=pet_owner.id)
                
                flash("Pet sucessfully added!", "success") 
            
        total_pets += 1    
           
        return render_template("add_dog.html", total_pets = total_pets, fname =user.fname,  pets_registered = pets_registered, num_pets = num_pets, user = user, user_id = user.user_id, pet_owner=pet_owner)

    flash(f"You currently have {total_pets} dogs registered under your profile", "info")
    
    return redirect(url_for("show_all_dogs", user_id=user_id))


@app.route("/create_booking/<user_id>")
def get_booking_form(user_id):
    """get booking form"""
            
    if "user_email" not in session:
        return redirect('/')
    
    else: 
        if crud.petowner_exists(user_id):
            pet_owner = crud.get_petowner_by_user_id(user_id)
            pet_owner_id = pet_owner.id
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
    
    if "user_email" in session:
        
        email = session.get('user_email')
        user = crud.get_user_by_email(email)
        user_id = user.user_id
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
        

        starttime_with_date = start_date + "T" + start_time
        starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

        endtime_with_date = start_date + "T" + end_time
        endtime_datetime = datetime.strptime(endtime_with_date, "%Y-%m-%dT%H:%M")

        booking = crud.create_booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=end_date, start_time=starttime_datetime, end_time=endtime_datetime, weekly=weekly)
        
        flash("booking sucessfully created", "success")

        
        return redirect(url_for("get_user_dashboard", user_id = user_id))
    return redirect('/')
    
  
@app.route('/sitters/<user_id>')
def all_sitters(user_id):
    """View all sitters in db"""
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)

    sitters = crud.get_all_other_sitters(user_id)
    users = crud.get_all_other_users(user_id)
    # for user in users:
    sitter_pics = []
    
    for sitter in sitters:
        public_id = sitter.user.profile_pic
        
        try:   
            cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        #  if profile pic not uploaded in cloudinary, set profile pic to user.profile_pic (assigned as public id)
        except:
            profile_pic = public_id
        # if profile pic in cloudinary, set it to the secure_url, in order to retrive it
       
        else:
            if 'secure_url' in cloud_pic:
                profile_pic = cloud_pic['secure_url']

        # cloud_pic = cloudinary.api.resources_by_ids(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        cloud_pic = cloudinary.api.resources(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        if 'secure_url' in cloud_pic:
            profile_pic = cloud_pic['secure_url']
        
        sitter_pics.append(profile_pic)
                 
    return render_template("all_sitters.html", sitter_pics=sitter_pics, sitters=sitters)


@app.route('/sitter_details/<sitter_id>')
def show_sitter_details(sitter_id):
    """Display a specific sitter information, using it's primary key"""
    
    sitter = crud.get_sitter_by_id(sitter_id)
    user = crud.get_user_by_sitter_id(sitter_id)
    
    public_id =  user.profile_pic   
    resources = cloudinary.api.resources_by_ids()
    if resources['public_id'] == public_id:
        print(f"im resources pi", resources['public_id'])
        cloud_pic = cloudinary.api.resource(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME, public_id=public_id)
        if 'secure_url' in cloud_pic:
            profile_pic = cloud_pic['secure_url']
        
    return render_template("sitter_details.html", sitter = sitter, user = user, profile_pic = profile_pic)


@app.route("/all_my_dogs/<user_id>")
def show_all_dogs(user_id):
    """return all the dogs under a specific pet_id"""

    if 'user_email' in session:
        
        if crud.petowner_exists(user_id):
            user = crud.get_user_by_id(user_id)
            pet_owner = crud.get_petowner_by_user_id(user_id)
            pet_owner_id = pet_owner.id
            my_pets = crud.get_pets_by_ownerid(pet_owner_id)
            
            if my_pets == 0:
                total_pets = 0
                
                flash("Sorry you don't have any dogs registered yet", "danger")
                
                return render_template("add_dog.html", user = user, pet_owner = pet_owner, total_pets = total_pets, pet_owner_id = pet_owner_id )
            else:                 
                
                return render_template("all_my_dogs.html", my_pets = my_pets, pet_owner_id = pet_owner_id)

        else:
            
            return redirect(url_for("petowner_signup", user_id = user_id))


    
    return redirect('/')
            

@app.route("/my_bookings/<user_id>")
def get_all_bookings(user_id):
    """Return all the bookings made by a specific user"""
    
    sitter_bookings = False
    pet_owner_bookings = False
    if "user_email" in session: 
        
        email = session['user_email']
        user = crud.get_user_by_email(email)
        
# check of pet_owner exists to then fetch pet_owner bookings, if  any.
        if crud.petowner_exists(user_id):
            pet_owner_bookings = crud.get_owner_bookings_by_user_id(user_id)

# check of sitter exists to then fetch sitters bookings, if  any.
        if crud.sitter_exists(user_id):
            sitter_bookings = crud.get_sitter_bookings_by_user_id(user_id)

        if not pet_owner_bookings or sitter_bookings:
            flash("Sorry you don't have any bookings yet", "info")
            
        return render_template("all_my_bookings.html", user = user, sitter_bookings = sitter_bookings, pet_owner_bookings = pet_owner_bookings)



# @app.route("/calendar")
# def calendar():
#    """remove the user from the session if it is there"""
   

#    return render_template("calendar_appointment-booking.html")


# #############################################

# # @app.route('users/<user_id>/availability')
# # def get_users_calendar(user_id):
    
# #     calendar = service.calendars().get(calendarId='primary').execute()

# # print calendar['summary']

@app.route("/logout")
def logout():
    """remove the user from the session if it is there"""
   
    if 'user_email' in session:
        session.pop('user_email', None)
        
    return redirect('/')

@app.route('/forgot_password', methods=["GET"])
def forgotPassword():
    """render forgot my password page"""

    return render_template("forgot_password.html")


@app.route("/delete/<user_id>")
def confirm_delete_user(user_id):
    "Ask user to confirm if they want to delete their profile"
    
    user = crud.get_user_by_id(user_id)
    
    get_profile_page(user_id)
    
    
    return redirect(url_for("get_profile_page", user_id=user_id))
    
    
@app.route("/delete/<user_id>", methods=['POST'])
def delete_user(user_id):
    "delete a user profile from database"
    
    if 'user_email' in session:
        
        delete_profile = request.form.get('delete')
        if 'DELETE' in delete_profile:
            user = crud.get_user_by_id(user_id)
            db.session.delete(user)
            db.session.commit()
            
            flash("Your profile was sucessfully deleted. To keep using your services, please sign up again!", "sucess")
    else:
        flash("Something went wrong, please log in and try again.", "warning")
    
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
#     
    
#     app.run('localhost', 5000, debug=True)

