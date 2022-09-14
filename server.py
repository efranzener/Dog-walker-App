

from __future__ import print_function

from http import server
from ipaddress import v6_int_to_packed
from tracemalloc import reset_peak
from flask import (Flask, render_template, request, flash, session, redirect, url_for, logging, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from sqlalchemy.sql import exists
from sqlalchemy import inspect
import datetime as dt
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import pytz

# import datetime
import os.path
import flask

# GOOGLE CALENDAR API IMPORTS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
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


def get_consent():
    """get user consent to accessing sensitive data"""
    
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
    except HttpError as error:
        print('An error occurred: %s' % error)
    return (service)
        
    
          
def get_available_sitters(user_id):
    
    service = get_consent()
    
    # get available sitters if user want to search for a specific date and time
    start_date = request.form.get("start_date")
    start_time = request.form.get("start_time")
    print("im the start_date", start_date)
    starttime_with_date = start_date + "T" + start_time
    starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

    # create an interval to calculate end time, based on 30 min walks
    interval = dt.timedelta(minutes=30)
    end_time =  starttime_datetime + interval
    
    user = crud.get_user_by_id(user_id)
    sitters = crud.get_all_other_sitters(user_id)
    cal_ids = []
    for sitter in sitters:
        calendar_ids={
            "id":sitter.user.email}
        cal_ids.append(calendar_ids)
       
    tz = pytz.timezone('US/Central')    
    start_datetime = tz.localize(starttime_datetime)
    end_datetime = tz.localize(end_time)
    body = {
        "timeMin": start_datetime.isoformat(),
        "timeMax": end_datetime.isoformat(),
        "timeZone": 'US/Central',
        "items": cal_ids
    }
    eventsResult = service.freebusy().query(body=body).execute()
    print("events result: ", eventsResult)
    cal_dict = eventsResult['calendars']
    
    available_sitters = []
    for cal_name in cal_dict:
        if cal_dict[cal_name] != []:
            available_sitters.append(cal_name)
            
        print(jsonify(cal_dict))
    return available_sitters


    
    # service = build('calendar', 'v3', credentials=get())

    # # Call the Calendar API
    # event = service.events().get(calendarId='testuser.numone@gmail.com', eventId='Busy').execute()

    # print (event['summary'])
    # # calendar = service.calendars().get(calendarId='{user.email}').execute()
    
    


            

    #         # Prints the start and name of the next 10 events
    #     #     for event in calendar:
    #     #         start = event['start'].get('dateTime', event['start'].get('date'))
    #     #         print(start, event['summary'])

    #     # except HttpError as error:
    #     #     print('An error occurred: %s' % error)


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
        session["user_email"] = user.email
        flash(f"Welcome, {user.fname}!", "primary")
        
        
        return redirect(url_for("get_user_dashboard", user_id=user_id, fname=user.fname))


@app.route('/user_dashboard/<user_id>')
def get_user_dashboard(user_id):
    """Show user dashboard"""

    user = crud.get_user_by_id(user_id)
    

    return render_template("user_dashboard.html", user = user)

@app.route('/calendar/<user_id>')
def get_user_calendar(user_id):
    """show user their own calendar"""
    
    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
         # google calendar id is the first part of the user email. In order to get that, we split the user email using the split() method
        split_email = user.email.split("@")
        
        # create a variable to store the calendar id(splitted email)
        calendar_id = split_email[0]
        
    return render_template('calendar.html', user = user, calendar_id = calendar_id)
    

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
        
       
        res = requests.get(f"https://{API_KEY}:{API_SECRET}@api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image")
        data = res.json()
        items = data['resources']
        
        current_pic = {}
        for item in items:
            if user.profile_pic == item['public_id']:
                current_pic = {
                    'profile_pic': user.profile_pic,
                    'public_id': item['public_id'],
                    'pic_url': item['url']
                }
                
        print("i'm the current user.profile pic", user.profile_pic, "my public id", item['public_id'] )   
             
        print("i'm the old user profile pic", current_pic) 
            
        return render_template("user_profile_page.html", profile_url = current_pic['pic_url'], profile_pic = current_pic['profile_pic'], pet_owner = pet_owner, sitter = sitter, user = user)
    
    
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
         
        
        res = requests.get(f"https://{API_KEY}:{API_SECRET}@api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image")
        data = res.json()
        items = data['resources']
        
        current_pic = {}
        for item in items:
            if user.profile_pic == item['public_id']:
                current_pic = {
                    'profile_pic': user.profile_pic,
                    'public_id': item['public_id'],
                    'pic_url': item['url']
                }
                
            print("i'm the current user.profile pic", user.profile_pic)        
            print("i'm the old user profile pic", current_pic) 
            
        return render_template('update_profile.html',  profile_url = current_pic['pic_url'], profile_pic = current_pic['profile_pic'], pet_owner = pet_owner, sitter = sitter, user = user)
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
        new_profile_file = request.files['profilepic']
        file_name = secure_filename(new_profile_file.filename)
        print("I'm profile_file", new_profile_file, file_name)
        
        if new_profile_file:
            # set UUID
            user.profile_pic = str(uuid.uuid1()) + "_" + file_name
            upload_result = cloudinary.uploader.upload(new_profile_file, public_id=user.profile_pic)

        else:
            user.profile_pic = user.profile_pic
            
            # cloud_pic = cloudinary.api.resources(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME)
        res = requests.get(f"https://{API_KEY}:{API_SECRET}@api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image")
        data = res.json()
        items = data['resources']
        
        current_pic = {}
        for item in items:
            if user.profile_pic == item['public_id']:
                current_pic = {
                    'profile_pic': user.profile_pic,
                    'public_id': item['public_id'],
                    'pic_url': item['url']
                }
                
        print("i'm the current user.profile pic", user.profile_pic)        
        print("i'm the old user profile pic", current_pic) 
        
        db.session.commit()
        flash("Your user information was sucessfully updated", "success")
                
        return redirect(url_for("get_profile_page", user_id = user_id))
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
            profile_file = request.files["profilepic"]
    
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
            

    flash(f"You currently have {total_pets} dogs registered under your profile", "info")
    
    return redirect(url_for("show_all_dogs", user_id=user_id))


@app.route("/create_booking/<user_id>")
def get_booking_form(user_id, sitter_id=0):
    """get booking form"""
   
    sitter_id = request.args.get('sitter_id')
    
    if sitter_id:
            print(sitter_id)
            sitter = crud.get_sitter_by_id(sitter_id)
            print(sitter)
            split_email = sitter.user.email.split("@")
            sitter_calendar_id = split_email[0]
            print("my sitter_id after if statement", sitter_id)
    else:
        sitter_id = 0         
    if "user_email" in session:

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
        
        return render_template("new_booking.html", sitter_calendar_id = sitter_calendar_id, pet_owner = pet_owner, sitter = sitter, sitters = sitters, user_id = user_id, pets = pets)    
    
    return redirect('/')
    
    
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
        sitter_id = request.form.get("sitter.id")
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
    
@app.route('/search_availability/<user_id>', methods=["POST"])
def display_available_sitters(user_id):
    """display sitters available on a specific time based on user search"""
    
    
    if 'user_email' in session:
        
        available_sitters_email = get_available_sitters(user_id)
        
        if available_sitters_email == []:
            flash("I'm sorry there is no sitters available in the time you selected, please try searching for a different time", "warning")
        
        else:
            print("Im the available sitter", available_sitters_email)
            cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
            api_secret = API_SECRET)

            current_user = crud.get_user_by_id(user_id)
            cloud_pic = cloudinary.api.resources(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME)
            res = requests.get(f"https://{API_KEY}:{API_SECRET}@api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image")
            data = res.json()
            pics = data['resources']
            sitters=[]
            
            all_users = []
            all_sitters = []
            #print('im the sitters', type(all_sitters))
            
        
            for email in available_sitters_email:
                available_user = crud.get_user_by_email(email)
                available_sitter = crud.get_sitter_by_user_id(available_user.user_id)
                all_users.append(available_user)
                all_sitters.append(available_sitter)
            print("available_sitters_email wasn't empty. all_users: ", all_users)
            
            for user in all_users:
                print(user)
                pet_sitter={}
                for sitter in all_sitters:
                    print(sitter)
                    split_email = user.email.split("@")
                    for item in pics:
                        if user.profile_pic == (item['public_id']):
                            pet_sitter['id'] = sitter.id
                            pet_sitter['fname'] = user.fname
                            pet_sitter['lname'] = user.lname
                            pet_sitter['pic'] = item['url']
                            pet_sitter['experience'] = sitter.years_of_experience
                            pet_sitter['rate'] = sitter.rate
                            pet_sitter['calendar_id'] = split_email[0]
                            pet_sitter['user_id'] = user.user_id
                        
                print("im the user.profile_pic", user.profile_pic)
        
                sitters.append(pet_sitter) 
            
            print("im sitters after the loops", sitters)   
            return render_template("all_sitters.html", sitters = sitters, current_user = current_user)

        return redirect (url_for("all_sitters", user_id = user_id))
    
    return redirect('/')
            
    
    
@app.route('/sitters/<user_id>')
def all_sitters(user_id):
    """View all sitters in db"""
    
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)

    current_user = crud.get_user_by_id(user_id)
    
    
    cloud_pic = cloudinary.api.resources(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME)
    res = requests.get(f"https://{API_KEY}:{API_SECRET}@api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image")
    data = res.json()
    pics = data['resources']
    sitters=[]
    
    all_users = []
    all_sitters = []
    
    all_users = crud.get_all_other_users(user_id)
    all_sitters = crud.get_all_other_sitters(user_id)
        
        
    print('all_users', all_users)
    
    for sitter in all_sitters:
        pet_sitter={}
        split_email = sitter.user.email.split("@")
        for item in pics:
            if sitter.user.profile_pic == (item['public_id']):
                pet_sitter['id'] = sitter.id
                pet_sitter['fname'] = sitter.user.fname
                pet_sitter['lname'] = sitter.user.lname
                pet_sitter['pic'] = item['url']
                pet_sitter['experience'] = sitter.years_of_experience
                pet_sitter['rate'] = sitter.rate
                pet_sitter['calendar_id'] = split_email[0]
                pet_sitter['user_id'] = sitter.user.user_id
                
                
        sitters.append(pet_sitter) 
    return render_template("all_sitters.html", sitters = sitters, current_user = current_user)



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
                cloud_pic = cloudinary.api.resources(api_key = API_KEY, api_secret = API_SECRET, cloud_name = CLOUD_NAME)
                res = requests.get(f"https://{API_KEY}:{API_SECRET}@api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image")
                data = res.json()
                pics = data['resources']
                pets=[]
                
                for pet in my_pets:
                    dog={}
                    for item in pics:
                        if pet.profile_pic == (item['public_id']):
                            dog['name'] = pet.name
                            dog['id'] = pet.pet_id
                            dog['pic'] = item['url']
                            dog['age'] = pet.age
                            dog['breed'] = pet.breed
                            dog['size'] = pet.size
                    pets.append(dog) 
                    print("my dog is", dog)
                print("my pets are", pets)

                return render_template("all_my_dogs.html", pets = pets, my_pets = my_pets, user = user, pet_owner_id = pet_owner_id)

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

