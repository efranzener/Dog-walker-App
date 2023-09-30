from __future__ import print_function
from http import server
from flask import (Flask, render_template, request, flash, session, redirect, url_for)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import datetime as dt
from datetime import datetime, timedelta
import os
import pytz

import os.path
import flask
from flask_bcrypt import generate_password_hash, check_password_hash


# GOOGLE CALENDAR API IMPORTS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


#  Cloudinary API imports
import cloudinary
import cloudinary.uploader
import cloudinary.api


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


# Google Calendar API
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
    """ query for available sitters based on Google Calendar"""
    
    service = get_consent()
   
    start_date = request.form.get("start_date")
    start_time = request.form.get("start_time")
    
    starttime_with_date = start_date + "T" + start_time
    starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

    # create an interval to calculate end time, based on 30 min walks
    interval = dt.timedelta(minutes=30)
    end_time =  starttime_datetime + interval
    
    # user = crud.get_user_by_id(user_id)
    sitters = crud.get_all_other_sitters(user_id)
    cal_ids = []
    for sitter in sitters:
        calendar_ids={
            "id":sitter.user.email}
        cal_ids.append(calendar_ids)
       
    tz = pytz.timezone('US/Pacific')    
    start_datetime = tz.localize(starttime_datetime)
    end_datetime = tz.localize(end_time)
    body = {
        "timeMin": start_datetime.isoformat(),
        "timeMax": end_datetime.isoformat(),
        "timeZone": 'US/Pacific',
        "items": cal_ids
    }
    eventsResult = service.freebusy().query(body=body).execute()
    
    cal_dict = eventsResult['calendars']
    available_sitters = []
    for cal_name in cal_dict:
        cal_busy = cal_dict[cal_name]['busy']
    
        if cal_busy != []:
            continue
        else:
            available_sitters.append(cal_name)

    return available_sitters


@app.route('/')
def homepage():
    """display the homepage"""
    
    return render_template("homepage.html")


@app.route('/signup')
def get_signup():
    """get user signup form"""
    
    return render_template("signup.html", states=states)


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
    confirm_password = request.form.get("password")
    mobile = request.form.get("mobile")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    profile_file = request.files['profilepic']
    

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Please try again.", "danger")    
    if password != confirm_password:
        flash("Please make sure your password and confirm password match.", "danger")

    if password == confirm_password:
        upload_result = cloudinary.uploader.upload(profile_file)
        data = upload_result
        profile_pic = data['url']

        user = crud.create_user(fname=fname, lname=lname, dob=dob, email=email, password=generate_password_hash(password).decode("utf-8"), mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic)
        
        flash("Account sucessfully created! Please login.", "success")
        
    return redirect('/')


@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    # user = crud.get_user_by_email(email)
    
    if password and email:
        user = crud.get_user_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                user_id = user.user_id
                session["user_email"] = user.email
                flash(f"Welcome, {user.fname}!", "primary")
                return redirect(url_for("get_user_dashboard", user_id=user_id, fname=user.fname))
            else:
                flash("Something went wrong. Please check your email and password and try again", "danger")

    else:
        flash("Something went wrong. Please check your email and password and try again", "danger")
        
    return redirect('/')    


@app.route('/user_dashboard/<user_id>')
def get_user_dashboard(user_id):
    """Show user dashboard"""
      
    pet_owner_bookings = False
    sitter_bookings = False
    if "user_email" in session: 
        
        user = crud.get_user_by_id(user_id)
        current_datetime = datetime.now()

        if crud.petowner_exists(user_id):
            
            pet_owner_bookings = crud.get_owner_bookings_by_user_id(user_id)
            
            next_pet_bookings=[]
            for booking in pet_owner_bookings:
                booking1 = {}
                if booking.start_time >= current_datetime and booking.start_date <= current_datetime + timedelta(days=7):
                    booking1['pet_name'] = booking.pet.name
                    booking1['date'] = booking.start_time.strftime("%A:" "%m/%d/%Y")
                    booking1['hour'] = booking.start_time.strftime("%H:%M")
                    booking1['sitter'] = booking.sitter.user.fname = " " + booking.sitter.user.lname

                    next_pet_bookings.append(booking1)
            
            if not pet_owner_bookings:
                pet_owner_bookings = False    
        else:
            next_pet_bookings=[]
        if crud.sitter_exists(user_id):
            sitter_bookings = crud.get_sitter_bookings_by_user_id(user_id)
            week_sitter_bookings=[]     
            for booking in sitter_bookings:
                booking2 = {}
                if booking.start_time >= current_datetime and booking.start_date <= current_datetime + timedelta(days=7):
                    booking2['pet_name'] = booking.pet.name
                    booking2['date'] = booking.start_date.strftime("%m/%d/%Y")
                    booking2['day'] = booking.start_time.strftime("%A:")
                    booking2['hour'] = booking.start_time.strftime("%H:%M")
                    booking2['address'] = booking.pet_owner.user.address + booking.pet_owner.user.city

                    week_sitter_bookings.append(booking2)
                    
            if not sitter_bookings:
                sitter_bookings = False   
        else:
            week_sitter_bookings= []
       
        return render_template("user_dashboard.html",  sitter_bookings = sitter_bookings, week_sitter_bookings = week_sitter_bookings, pet_owner_bookings = pet_owner_bookings, next_pet_bookings = next_pet_bookings, user = user)
    return redirect('/')


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
            
            flash("Sitter profile already created. Here you can update any information you wish", "info")
            
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
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(user_id)
        if sitter:
            sitter = crud.get_sitter_by_user_id(user_id)
        
        current_pic = {
            'profile_pic': user.profile_pic,
            'pic_url': user.profile_pic
            }

        return render_template("user_profile_page.html", profile_url=current_pic['pic_url'], profile_pic=current_pic['profile_pic'], pet_owner=pet_owner, sitter=sitter, user=user)

    return redirect('/')
    
    
@app.route("/user_profile/<user_id>/update")
def get_profile_update_form(user_id):
    """get profile update form"""

    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        sitter = crud.sitter_exists(user_id)
        pet_owner = crud.petowner_exists(user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(user_id)
            
        if sitter:
            sitter=crud.get_sitter_by_id(user_id)
         
        
        current_pic = {
        'profile_pic': user.profile_pic,
        'pic_url': user.profile_pic
        }
    
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
        
        if new_profile_file:
            upload_result = cloudinary.uploader.upload(new_profile_file)
            data = upload_result
            user.profile_pic = data['url']

        else:
            user.profile_pic = user.profile_pic

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
            
            flash("Pet owner profile already created. Here you can update any information you wish", "info")
            
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
        
        flash("Your pet owner profile was sucessfully updated!", "success")
        
        return redirect(url_for('get_profile_page', user_id = user_id))
    
    return redirect('/')
    
    
@app.route("/add_dog/<user_id>", methods=["GET", "POST"])
def create_pet_profile(user_id):
    """create a new dog profile"""
    
    if 'user_email' in session:
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
            flash("Finish your pet owner profile to be able to add a pet", "info")

            return redirect(url_for("petowner_signup", user_id = user_id))
        
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
    
            if crud.pet_exists(pet_owner_id, name):
    
                flash("Pet already created. Sorry, at this moment we don't support changes in the pet profile", "info")
                return url_for("show_all_dogs", user_id=user_id )
            else:
                upload_result = cloudinary.uploader.upload(profile_file)
                data = upload_result
                profile_pic = data['url'] 
                                    
                pet = crud.create_pet(name= name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, house_trained=house_trained, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, additional_info=additional_info, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owner_id=pet_owner.id)
                
                flash("Pet sucessfully added!", "success") 
                
                total_pets += 1    
            
            flash(f"You currently have {total_pets} dogs registered under your profile", "info")

            return redirect(url_for("show_all_dogs", user_id=user_id))
    return redirect('/')


@app.route("/create_booking/<user_id>")
def get_booking_form(user_id):
    """get booking form"""
   
    selected_sitter_id = request.args.get('sitter_id')
    
    if selected_sitter_id:
        
        selected_sitter = crud.get_sitter_by_id(selected_sitter_id)
        split_email = selected_sitter.user.email.split("@")
        sitter_calendar_id = split_email[0]
    else:
        selected_sitter_id = 0   
        sitter_calendar_id = 0 
        selected_sitter = None
        
    if "user_email" in session:

        if crud.petowner_exists(user_id):
            user = crud.get_user_by_id(user_id)
            pet_owner = crud.get_petowner_by_user_id(user_id)
            pet_owner_id = pet_owner.id
            sitters = crud.get_all_other_sitters(user_id)
            pet_owner = crud.get_petowner_by_user_id(user_id)
            pet_owner_id = pet_owner.id
            if crud.get_total_pets_by_owner(pet_owner_id) > 0:
                pets = crud.get_pets_by_ownerid(pet_owner_id)
            else:
                flash("Please register your dog(s) to be able to book a walk", "info")
                
                return redirect(url_for("create_pet_profile", user_id = user_id)) 
        else:
            flash("Please finish your pet owner profile to be able to book", "info")

            return redirect(url_for("petowner_signup", user_id = user_id))
        
        date_today = datetime.today().strftime("%m/%d/%Y")
        max_date = (datetime.today() + timedelta(days=60)).strftime("%m/%d/%Y")
        

        return render_template("new_booking.html",max_date = max_date, min_date=date_today, user=user, sitter_calendar_id = sitter_calendar_id, pet_owner = pet_owner, sitter = selected_sitter, sitters = sitters, user_id = user_id, pets = pets)    
    
    return redirect('/')


def create_cal_bokng(user_id, sitter_id, pet_id, address, description):
    """insert a new_booking into google calendar"""
    
    service = get_consent()
    
    user = crud.get_user_by_id(user_id)
    sitter = crud.get_user_by_id(sitter_id)
    pet_owner = crud.get_petowner_by_user_id(user_id)
    pet = crud.get_pet_by_id(pet_id)
    sitter_user = crud.get_user_by_id(sitter.user_id)
    pet_name = pet.name
    sitter_name = (sitter_user.fname) +" "+(sitter_user.lname)
    pet_owner_name = (user.fname) +" "+ (user.lname)
    
    start_date = request.form.get("start_date")
    start_time = request.form.get("start_time")
    starttime_with_date = start_date + "T" + start_time
    starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

    # create an interval to calculate end time, based on 30 min walks
    interval = dt.timedelta(minutes=30)
    end_time =  starttime_datetime + interval

    tz = pytz.timezone('US/Pacific')    
    start_datetime = tz.localize(starttime_datetime)
    end_datetime = tz.localize(end_time)
    body = {
        "summary":f"Dog Walk for {pet.name}" ,
        "description":description,
        "location": address,
        "transparency": "opaque",
        "visibility": "private",
        "start":{
            "dateTime": start_datetime.isoformat(),
            "timeZone": 'US/Pacific',
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": 'US/Pacific',
        },
        "attendees": [
            {'email': user.email},
            {'email': sitter_user.email},
        ],
        "reminders": {
            "useDefault": True
            }
    }
    
    event = service.events().insert(calendarId=sitter_user.email,  body=body).execute()
   
    return event
    
    
@app.route("/create_booking/<pet_owner_id>", methods=["POST"])
def create_booking(pet_owner_id):
    """ create a new booking"""
    
    if "user_email" in session:
            
        email = session.get('user_email')
        user = crud.get_user_by_email(email)
        user_id = user.user_id
       
        pet_owner_id = pet_owner_id
        sitter_id = request.form.get("sitter_id")
        pet_id = request.form.get("pet_id")
        start_date = request.form.get("start_date")
        start_time = request.form.get("start_time")
        end_date = start_date
        
        # info for creating the booking in google calendar
        address = request.form.get("address")
        description = request.form.get("description")

        # weekly = bool(request.form["weekly"])
        
        starttime_with_date = start_date + "T" + start_time
        starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")
        
        # create an interval to calculate end time, based on 30 min walks
        interval = dt.timedelta(minutes=30)
        endtime_with_date=  starttime_datetime + interval
        
        endtime_datetime = endtime_with_date
        booking = crud.create_booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=end_date, start_time=starttime_datetime, end_time=endtime_datetime, weekly=False)

        flash("Booking sucessfully created", "success")
        
        create_cal_bokng(user_id, sitter_id, pet_id, address = address, description = description)
        
        flash("Booking sucessfully added to your calendar", "success")

        return redirect(url_for("get_all_bookings", user_id = user_id))
    return redirect('/')
    
    
@app.route('/search_availability/<user_id>', methods=["POST"])
def display_available_sitters(user_id):
    """display sitters available on a specific time based on user search"""
    
    if 'user_email' in session:
        if request.method == 'GET':
            return redirect (url_for("all_sitters", user_id = user_id))
        
        available_sitters_email = get_available_sitters(user_id)
        if available_sitters_email == [] or not available_sitters_email:
            
            flash("There are no sitters available in the time you selected. Please try searching for a different time, or browing all the sitters in our database", "info")
        else:
            cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
            api_secret = API_SECRET)

            current_user = crud.get_user_by_id(user_id)
        
            sitters=[]
            all_sitters = []
            for email in available_sitters_email:
                user = crud.get_user_by_email(email)
                available_sitter = crud.get_sitter_by_user_id(user.user_id)
                all_sitters.append(available_sitter)
                
            for sitter in all_sitters:
                pet_sitter={}
                split_email = sitter.user.email.split("@")
                pet_sitter['id'] = sitter.id
                pet_sitter['fname'] = sitter.user.fname
                pet_sitter['lname'] = sitter.user.lname
                pet_sitter['pic'] = sitter.user.profile_pic
                pet_sitter['experience'] = sitter.years_of_experience
                pet_sitter['rate'] = sitter.rate
                pet_sitter['calendar_id'] = split_email[0]
                pet_sitter['user_id'] = sitter.user.user_id
                pet_sitter['summary'] = sitter.summary
                sitters.append(pet_sitter)        
        
            return render_template("all_sitters.html", sitters = sitters, user = current_user)

        return redirect (url_for("all_sitters", user_id = user_id))
    
    return redirect('/')
            
    
@app.route('/sitters/<user_id>')
def all_sitters(user_id):
    """View all sitters in db"""
    
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)

    current_user = crud.get_user_by_id(user_id)
    all_sitters = crud.get_all_other_sitters(user_id)
    
    sitters=[]

    for sitter in all_sitters:
        pet_sitter = {}
        split_email = sitter.user.email.split("@")
        pet_sitter['id'] = sitter.id
        pet_sitter['fname'] = sitter.user.fname
        pet_sitter['lname'] = sitter.user.lname
        pet_sitter['pic'] = sitter.user.profile_pic
        pet_sitter['experience'] = sitter.years_of_experience
        pet_sitter['rate'] = sitter.rate
        pet_sitter['calendar_id'] = split_email[0]
        pet_sitter['user_id'] = sitter.user.user_id
        pet_sitter['summary'] = sitter.summary
                
        sitters.append(pet_sitter) 
    
    return render_template("all_sitters.html", sitters = sitters, user = current_user)


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
                
                flash("You haven't registered any dogs registered yet", "info")
                
                return render_template("add_dog.html", user = user, pet_owner = pet_owner, total_pets = total_pets, pet_owner_id = pet_owner_id )
            else:
                pets=[]
                for pet in my_pets:
                    dog={}
                    dog['name'] = pet.name
                    dog['id'] = pet.pet_id
                    dog['pic'] = pet.profile_pic
                    dog['age'] = pet.age
                    dog['breed'] = pet.breed
                    dog['size'] = pet.size
                    dog['allergies'] = pet.allergies
                    dog['allergies_kind'] = pet.allergies_kind
                    dog['friendly_w_dogs'] = pet.friendly_w_dogs
                    dog['house_trained'] = pet.friendly_w_kids
                    dog['spayed_neutered'] = pet.spayed_neutered
                    dog['shouse_trained'] = pet.house_trained
                    dog['microchipped'] = pet.microchipped
                    dog['additional_info'] = pet.additional_info
                    
                    pets.append(dog) 

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
        
        user = crud.get_user_by_id(user_id)
        split_email = user.email.split("@")
        calendar_id = split_email[0]

        owner_bkngs = []
        if crud.petowner_exists(user_id):
            pet_owner_bookings = crud.get_owner_bookings_by_user_id(user_id)
            
            for booking in pet_owner_bookings:
            
                info_sitter={}
                info_sitter['booking_id'] = booking.id
                info_sitter['dog_name'] = booking.pet.name 
                info_sitter['sitter_pic'] = booking.sitter.user.profile_pic
                info_sitter['experience'] = booking.sitter.years_of_experience
                info_sitter ['summary'] = booking.sitter.summary
                info_sitter['date'] = booking.start_date.strftime("%m/%d/%Y")
                info_sitter['time'] = booking.start_time.strftime("%H:%M")
                info_sitter['sitter_name'] = booking.sitter.user.fname + " " + booking.sitter.user.lname
                info_sitter['sitter_mobile'] = booking.sitter.user.mobile
                info_sitter['sitter_email']  = booking.sitter.user.email
                
                owner_bkngs.append(info_sitter)
                
        # check of sitter exists to then fetch sitters bookings, if  any.
        sitter_bkngs=[]
        if crud.sitter_exists(user_id):
            sitter_bookings = crud.get_sitter_bookings_by_user_id(user_id)
      
            
            for booking in sitter_bookings:
                info={}
                
                info['dog_name'] = booking.pet.name
                info['dog_pic'] = booking.pet.profile_pic
                info['age'] = booking.pet.age
                info['breed'] = booking.pet.breed
                info['size'] = booking.pet.size
                info['allergies'] = booking.pet.allergies
                info['allergies_kind'] = booking.pet.allergies_kind
                info['friendly_w_dogs'] = booking.pet.friendly_w_dogs
                info['house_trained'] = booking.pet.friendly_w_kids
                info['spayed_neutered'] = booking.pet.spayed_neutered
                info['house_trained'] = booking.pet.house_trained
                info['microchipped'] = booking.pet.microchipped
                info['additional_info'] = booking.pet.additional_info
                info['date'] = booking.start_date.strftime("%m/%d/%Y")
                info['time'] = booking.start_time.strftime("%I:%M %p")
                info['booking_id'] =  booking.id
                info['calendar_id'] = calendar_id
                info['address'] = booking.pet_owner.user.address +", "+ booking.pet_owner.user.city +"-"+ booking.pet_owner.user.state
                info['emergency_name'] = booking.pet.emergency_contact_name
                info['emergency_relationship'] = booking.pet.emergency_contact_relationship
                info['emergency_phone'] = booking.pet.emergency_phone
                info['owner_name'] = booking.pet_owner.user.fname + " " + booking.pet_owner.user.lname
                info['owner_phone'] = booking.pet_owner.user.mobile
                sitter_bkngs.append(info)
   
        elif not pet_owner_bookings or not sitter_bookings:
            flash("You haven't made any bookings yet", "info")
        return render_template("all_my_bookings.html", owner_bkngs=owner_bkngs, sitter_bkngs=sitter_bkngs, user = user, sitter_bookings = sitter_bookings, pet_owner_bookings = pet_owner_bookings)
    return redirect("/")


@app.route("/logout")
def logout():
    """remove the user from the session if it is there"""
   
    if 'user_email' in session:
        session.pop('user_email', None)
        
    return redirect('/')


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
            if crud.petowner_exists(user_id):
                pet_owner = crud.get_petowner_by_user_id(user_id)
                db.session.delete(pet_owner)
                db.session.commit()

            if crud.sitter_exists(user_id):
                sitter = crud.get_sitter_by_user_id(user_id)
                db.session.delete(sitter)
                db.session.commit()

            user = crud.get_user_by_id(user_id)
            db.session.delete(user)
            db.session.commit()
            
            flash("All your profile(s) were sucessfully deleted. To keep using your services, please sign up again!", "success")
        else:
            return redirect(url_for("get_profile_page", user_id = user_id))
    else:
        flash("Something went wrong, please log in and try again.", "warning")
    
    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


