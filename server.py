from __future__ import print_function

from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)

from flask_login import LoginManager, login_user, login_required, fresh_login_required, logout_user

from itsdangerous import URLSafeSerializer
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import datetime as dt
from datetime import datetime, timedelta
import os


import gcalendar
# from os import path, environ

import pytz
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
configr = cloudinary.config(secure=True)
API_KEY = os.environ['cloudinary_api_key']
API_SECRET = os.environ['api_secret']
CLOUD_NAME = os.environ['cloud_name']


# Google Calendar API
# CLIENT_SECRETS_FILE = 'credentials.json'
# SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
# API_SERVICE_NAME = 'calendar'
# API_VERSION = 'v3'


app = Flask(__name__)
app.secret_key = os.environ['secret_key']
app.jinja_env.undefined = StrictUndefined
serializer = URLSafeSerializer(app.secret_key)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)


states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


###Flask Login###

login_manager = LoginManager()
login_manager.login_view = 'homepage'
login_manager.session_protection = "strong"
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(alternative_id):
    """Given an alternative id, return the associated User object"""

    return crud.get_user_by_alternative_id(alternative_id)
  

# # Google Calendar API
# def get_consent():
#     """get user consent to accessing sensitive data"""
    
#     creds = None
    
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
            
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     try:
#         service = build('calendar', 'v3', credentials=creds)
#     except HttpError as error:
#         print('An error occurred: %s' % error)
    
#     return service

   



@app.route('/')
@app.route('/homepage')
def homepage():
    """display the homepage"""

    if 'user_email' in session:
        
        email = session["user_email"]
        current_user = crud.get_user_by_email(email)
        return redirect (url_for("get_user_dashboard", alternative_id=current_user.alternative_id))
    else: 
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
    pwd = request.form.get("password")
    confirm_pwd= request.form.get("password")
    mobile = request.form.get("mobile")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    profile_file = request.files['profilepic']
    

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Please try again.", "danger")

    if pwd != confirm_pwd:
        flash("Please make sure your password and confirm password match.", "danger")

    if pwd == confirm_pwd:

        upload_result = cloudinary.uploader.upload(profile_file)
        data = upload_result
        profile_pic = data['url']
        
        user = crud.create_user(fname=fname, lname=lname, dob=dob, email=email, password=generate_password_hash(pwd).decode("utf-8"), authenticated=False, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, profile_pic=profile_pic, alternative_id = serializer.dumps([email, pwd]))
        db.session.add(user)
        db.session.commit()
        flash("Account sucessfully created! Please login.", "success")
        
    return redirect('/')



@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    

    email = request.form.get("email")
    pwd = request.form.get("password")
    remember = request.form.get('rememberme')
    user = crud.get_user_by_email(email)
    
    if email and pwd:
        try:
            if check_password_hash(user.password, pwd):
                current_user = user
                if remember:
                    remember=True
                current_user.authenticated = True
                login_user(current_user, remember=remember)
                session["alternative_id"] = current_user.alternative_id
                session["user_email"] = current_user.email
    
                return redirect(url_for("get_user_dashboard", alternative_id = session["alternative_id"]))


            else:

                flash("Something went wrong. Please make sure your email and password are correct and try again", "danger")
        except:
                flash("Something went wrong. Please check your email and password and try again", "warning")
    return redirect('/')
  
        
@app.route('/user_dashboard/<alternative_id>')
@login_required
def get_user_dashboard(alternative_id):
    """Show user dashboard"""
     
    pet_owner_bookings = False
    sitter_bookings = False

    if 'user_email' in session: 
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        current_datetime = datetime.now()
        user_id = current_user.user_id
        if crud.petowner_exists(user_id):
            
            pet_owner_bookings = crud.get_owner_bookings_by_user_id(user_id)
            
            next_pet_bookings=[]
            for booking in pet_owner_bookings:
                booking1 = {}
                
                
                if booking.start_date >= current_datetime and booking.start_date <= current_datetime + timedelta(days=7):
                    booking1['pet_name'] = booking.pet.name
                    booking1['date'] = booking.start_date.strftime("%A:" "%m/%d/%Y")
                    booking1['hour'] = booking.start_time
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
                if booking.start_date >= current_datetime and booking.start_date <= current_datetime + timedelta(days=7):
                    booking2['pet_name'] = booking.pet.name
                    booking2['date'] = booking.start_date.strftime("%m/%d/%Y")
                    booking2['day'] = booking.start_date.strftime("%A:")
                    booking2['hour'] = booking.start_time
                    booking2['address'] = booking.pet_owner.user.address + booking.pet_owner.user.city
                    week_sitter_bookings.append(booking2)
                    
            if not sitter_bookings:
                sitter_bookings = False   
        else:
            week_sitter_bookings= []
       
        return render_template("user_dashboard.html",  sitter_bookings = sitter_bookings, week_sitter_bookings = week_sitter_bookings, pet_owner_bookings = pet_owner_bookings, next_pet_bookings = next_pet_bookings, current_user = current_user)
    return redirect('/')


@app.route('/calendar/<user_id>')
@login_required
def get_user_calendar(user_id):
    """show user their own calendar"""
    
    if 'user_email' in session:
        
        user = crud.get_user_by_id(user_id)
        
        # google calendar id is the first part of the user email. In order to get that, we split the user email using the split() method
        split_email = user.email.split("@")
        
        # create a variable to store the calendar id(splitted email)
        calendar_id = split_email[0]
        
    return render_template('calendar.html', user = user, calendar_id = calendar_id)
    

@app.route("/sitter_signup/<alternative_id>")
@login_required
def get_sitter_signup(alternative_id) :     
    """get sitter sign up form"""
    
    if 'user_email' in session:

        current_user = crud.get_user_by_alternative_id(alternative_id)
        
        if crud.sitter_exists(current_user.user_id):
            sitter = crud.get_sitter_by_user_id(current_user.user_id)
            
            flash("Sitter profile already created. Here you can update any information you wish", "info")
            
            return redirect(url_for("get_profile_page", sitter=sitter, user_id=current_user.user_id))
        
        else:
                
            return render_template("sitter_signup.html", current_user = current_user)  
    
    return('/')    
        
        
@app.route("/sitter_signup/<user_id>", methods=["POST"])
@login_required
def sitter_signup(user_id):     
    """create a new sitter profile"""
        
    if 'user_email' in session:
      
        user = crud.get_user_by_id(user_id)
        
        years_of_experience = request.form.get("experience")
        summary = request.form.get("summary")
        rate = request.form.get("rate")
        
        sitter = crud.create_sitter(user_id = user_id, years_of_experience = years_of_experience, summary = summary, rate = rate)
        db.session.add(sitter)
        db.session.commit()
        flash("Sitter profile sucessfully completed!", "success")
        
        return redirect(url_for("get_user_dashboard", user_id = user_id))
    
    return redirect('/')
    
  
@app.route("/user_profile/<alternative_id>")
@login_required
def get_profile_page(alternative_id):
    """display user profile page"""
    
    if 'user_email' in session:
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        sitter = crud.sitter_exists(current_user.user_id)
        pet_owner = crud.petowner_exists(current_user.user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
        if sitter:
            sitter = crud.get_sitter_by_user_id(current_user.user_id)
        
        current_pic = {
            'profile_pic': current_user.profile_pic,
            'pic_url': current_user.profile_pic
            }

        return render_template("user_profile_page.html", profile_url=current_pic['pic_url'], profile_pic=current_pic['profile_pic'], pet_owner=pet_owner, sitter=sitter, current_user=current_user)

    return redirect('/')
    
    
@app.route("/user_profile/<alternative_id>/update")
@login_required
def get_profile_update_form(alternative_id):
    """get profile update form"""

    if 'user_email' in session:
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        sitter = crud.sitter_exists(current_user.user_id)
        pet_owner = crud.petowner_exists(current_user.user_id)
        
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
            
        if sitter:
            sitter=crud.get_sitter_by_id(current_user.user_id)
         
    

        current_pic = {
        'profile_pic': current_user.profile_pic,
        'pic_url': current_user.profile_pic
        }
    
        return render_template('update_profile.html',  profile_url = current_pic['pic_url'], profile_pic = current_pic['profile_pic'], pet_owner = pet_owner, sitter = sitter, current_user = current_user)
    else:
        return redirect('/')
    
    
@app.route("/user_profile/<alternative_id>/update", methods=['POST'])
@fresh_login_required
def update_user_profile(alternative_id):
    """ update user profile page """
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)
    upload_result = None
    
    if 'user_email' in session:
        
        user = crud.get_user_by_alternative_id(alternative_id)
        current_user = crud.get_user_by_id(user.user_id)
        current_user.fname = request.form.get("fname")
        current_user.lname= request.form.get("lname")
        current_user.dob = request.form.get("dob")
        current_user.email = request.form.get("email")
        current_user.mobile = request.form.get("mobile")
        current_user.address = request.form.get("address")
        current_user.city = request.form.get("city")
        current_user.state = request.form.get("state")
        current_user.zip_code = request.form.get("zip_code")
        new_profile_file = request.files['profilepic']
        new_password = request.form.get("newpassword")
        new_confirm_password = request.form.get("new_confirmpassword")
        
        
        if new_profile_file:
            upload_result = cloudinary.uploader.upload(new_profile_file)
            data = upload_result
            current_user.profile_pic = data['url']

        else:
            current_user.profile_pic = current_user.profile_pic
        

        if not new_password and not new_confirm_password:
            user = crud.get_user_by_id(current_user.user_id)
            current_user.password = new_password
            current_user.confirm_password = new_confirm_password
   
        elif not new_password or not new_confirm_password:

            flash("please check you password and match password and try again", "danger")

            return redirect(url_for("update_user_profile", alternative_id = current_user.alternative_id, user_id = current_user.user_id))
        else:
            if new_password == new_confirm_password:
                
                alternative_id = serializer.dumps([current_user.email, current_user.password])

                current_user.password = generate_password_hash(new_password, rounds=12).decode("utf-8")
            else:
                flash("Please make sure your password and confirm password match", "danger")

                return redirect(url_for("update_user_profile", alternative_id = current_user.alternative_id, user_id = current_user.user_id))
    
        current_user.password = current_user.password
        db.session.commit()
        
        flash("Your user information was sucessfully updated", "success")
                
        return redirect(url_for("get_profile_page", alternative_id = current_user.alternative_id, user_id = current_user.user_id))
       

    redirect(url_for("get_profile_page", alternative_id = alternative_id, user_id = user.user_id))
    
    
@app.route("/sitter_profile/<alternative_id>/update", methods=['POST'])
@fresh_login_required
def update_sitter_profile(alternative_id):
    """ update sitter_profile_page """
    
    if 'user_email' in session:
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        sitter = crud.get_sitter_by_user_id(current_user.user_id)
        
        sitter.years_of_experience = request.form.get("experience")
        sitter.summary = request.form.get("summary")
        sitter.rate = request.form.get("rate") 
        
        db.session.commit()
        
        flash("Your sitter profile was sucessfully updated!", "success")
        
        return redirect(url_for('get_profile_page', alternative_id = alternative_id))
    
    return redirect('/')
        
   
@app.route("/petowner_signup/<alternative_id>")
@login_required
def petowner_signup_form(alternative_id):
    """ get pet owner sign up form """
   
    if 'user_email' in session:
        current_user = crud.get_user_by_alternative_id(alternative_id)
        sitter = crud.sitter_exists(current_user.user_id)
        pet_owner = crud.petowner_exists(current_user.user_id)
        
        
        if sitter:
            sitter=crud.get_sitter_by_user_id(current_user.user_id)
            
        if pet_owner:
            pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
            
            flash("Pet owner profile already created. Here you can update any information you wish", "info")
            
            return redirect(url_for("get_profile_page", alternative_id = alternative_id))
        
        return render_template("petowner_signup.html", current_user = current_user)
    
    return redirect('/') 


@app.route("/petowner_signup/<alternative_id>", methods=["POST"])
def petowner_signup(alternative_id):
    """ create a new pet owner"""
   
    if 'user_email' in session:
       
        num_pets = request.form.get("num_pets")
        current_user = crud.get_user_by_alternative_id(alternative_id)
        pet_owner = crud.create_pet_owner( user_id = current_user.user_id, num_pets = num_pets)
        
        db.session.add(pet_owner)
        db.session.commit()

        flash("Profile sucessfully created! Proceed to add your dog info.", "success")
            
        return redirect(url_for("create_pet_profile", user_id = current_user.user_id))
    
    return redirect('/')


@app.route("/petowner_profile/<alternative_id>/update", methods=['POST'])
@fresh_login_required
def update_petowner_profile(alternative_id):
    """ update pet owner profile page """
    
    if 'user_email' in session:
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
        pet_owner.num_pets = request.form.get("num_pets")
        
        db.session.commit()
        
        flash("Your pet owner profile was sucessfully updated!", "success")
        
        return redirect(url_for('get_profile_page', alternative_id = current_user.alternative_id))
    
    return redirect('/')
    
    
@app.route("/add_dog/<alternative_id>", methods=["GET", "POST"])
@login_required
def create_pet_profile(alternative_id):
    """create a new dog profile"""
    
    if 'user_email' in session:

        cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
        api_secret = API_SECRET)
        upload_result = None
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        
        if crud.petowner_exists(current_user.user_id):
            
            pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
            num_pets = pet_owner.num_pets
            pet_owner_id = pet_owner.id
            pets_registered = crud.get_pets_by_ownerid(pet_owner_id)
            total_pets = crud.get_total_pets_by_owner(pet_owner_id)

        else:
            flash("Finish your pet owner profile to be able to add a pet", "info")

            return redirect(url_for("petowner_signup", user_id = current_user.user_id))
        
        if request.method == "GET":
            return render_template("add_dog.html", total_pets = total_pets, fname = current_user.fname, pets_registered = pets_registered, num_pets = num_pets, user = current_user, user_id = current_user.user_id, pet_owner=pet_owner)
            
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
                return url_for("show_all_dogs", user_id=current_user.user_id )
            else:
                upload_result = cloudinary.uploader.upload(profile_file)
                data = upload_result
                profile_pic = data['url'] 
                                    
                pet = crud.create_pet(name= name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, house_trained=house_trained, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, additional_info=additional_info, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owner_id=pet_owner.id)
                db.session.add(pet)
                db.session.commit()   

                flash("Pet sucessfully added!", "success") 
                
                total_pets += 1    
            
            flash(f"You currently have {total_pets} dogs registered under your profile", "info")

            return redirect(url_for("show_all_dogs", user_id=alternative_id))
    return redirect('/')


@app.route("/create_booking/<alternative_id>")

@login_required
def get_booking_form(alternative_id):
    """get booking form"""
   
    selected_sitter_id = request.args.get('sitter_id')
    date = request.args.get('start_date')

    if selected_sitter_id:
        
        selected_sitter = crud.get_sitter_by_id(selected_sitter_id)
        split_email = selected_sitter.user.email.split("@")
        sitter_calendar_id = split_email[0]
    else:
        selected_sitter_id = 0   
        sitter_calendar_id = 0 
        selected_sitter = None
        
    if 'user_email' in session:
        current_user = crud.get_user_by_alternative_id(alternative_id)
        

        if crud.petowner_exists(current_user.user_id):

            user = crud.get_user_by_id(current_user.user_id)
            pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
            pet_owner_id = pet_owner.id
            sitters = crud.get_all_other_sitters(current_user.user_id)
            pet_owner = crud.get_petowner_by_user_id(current_user.user_id)
            pet_owner_id = pet_owner.id
            if crud.get_total_pets_by_owner(pet_owner_id) > 0:
                pets = crud.get_pets_by_ownerid(pet_owner_id)
            else:
                flash("Please register your dog(s) to be able to book a walk", "info")
                
                return redirect(url_for("create_pet_profile", user_id = current_user.user_id)) 
        else:
            flash("Please finish your pet owner profile to be able to book", "info")

            return redirect(url_for("petowner_signup", user_id = current_user.user_id))
        
        min_date= (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
        max_date = (datetime.today() + timedelta(days=60)).strftime("%m/%d/%Y")

        # if date:
        #     times_list = get_selected_date()
        #     print("im the times list", times_list)
        # else:
        #     times_list = False
        
        return render_template("new_booking.html", times = [], max_date=max_date, min_date=min_date, user=user, sitter_calendar_id = sitter_calendar_id, pet_owner = pet_owner, sitter = selected_sitter, sitters = sitters, alternative_id = alternative_id, pets = pets)    
    
    return redirect('/')




# def create_cal_bokng(user_id, sitter_id, pet_id, address, description):
#     """insert a new_booking into google calendar"""
    
#     service = get_consent()
    
#     user = crud.get_user_by_id(user_id)
#     sitter = crud.get_user_by_id(sitter_id)
#     pet = crud.get_pet_by_id(pet_id)
#     sitter_user = crud.get_user_by_id(sitter.user_id)
#     pet_name = pet.name
#     sitter_name = (sitter_user.fname) +" "+(sitter_user.lname)
#     pet_owner_name = (user.fname) +" "+ (user.lname)
    
#     start_date = request.form.get("start_date")
#     start_time = request.form.get("start_time")
#     starttime_with_date = start_date + "T" + start_time
    
#     starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

#     # create an interval to calculate end time, based on 30 min walks
#     interval = dt.timedelta(minutes=30)
#     end_time =  starttime_datetime + interval

#     tz = pytz.timezone('US/Pacific')    
#     start_datetime = tz.localize(starttime_datetime)
#     end_datetime = tz.localize(end_time)
#     body = {
#         "summary":f"Dog Walk for {pet.name}" ,
#         "description":description,
#         "location": address,
#         "transparency": "opaque",
#         "visibility": "private",
#         "start":{
#             "dateTime": start_datetime.isoformat(),
#             "timeZone": 'US/Pacific',
#         },
#         "end": {
#             "dateTime": end_datetime.isoformat(),
#             "timeZone": 'US/Pacific',
#         },
        
#         "attendes": [
#             {'email': user.email},
#             {'email': sitter_user.email},
            
#             {'petname': pet_name},
#             {'petOwner': pet_owner_name},
#             {'Sitter': sitter_name}
#         ],
#         "reminders": {
#             "useDefault": True
#             }
#     }
    
#     event = service.events().insert(calendarId=sitter_user.email,  body=body).execute()
    
#     return event
    
    
@app.route("/create_booking/<pet_owner_id>", methods=["POST"])
@login_required
def create_booking(pet_owner_id):
    """ create a new booking"""
    
    if 'user_email' in session:

        email = session.get('user_email')
        current_user = crud.get_user_by_email(email)
        user_id = current_user.user_id
       
        pet_owner_id = pet_owner_id
        sitter_id = request.form.get("sitter_id")
        pet_id = request.form.get("pet_id")
        date = request.form.get("start_date")
        start_time = request.form.get("start_time")
        end_date = date
        

        print("im the start_date", date, "type:", type(date))
        # info for creating the booking in google calendar
        address = request.form.get("address")
        description = request.form.get("description")

        # weekly = bool(request.form["weekly"])
        
       

        datetime_string = date + "T" + start_time
        start_date = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M")
        
        start_time = start_date.strftime("%I:%M %p")

        event = gcalendar.create_cal_bokng(start_date = start_date, start_time = start_time, user_id=user_id , sitter_id=sitter_id, pet_id=pet_id, address=address, description=description)
        flash("Booking sucessfully added to your calendar", "success")
        
        google_cal_id = event['id']
        
        booking = crud.create_booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=start_date + timedelta(minutes=30), start_time=start_time, end_time=((start_date + timedelta(minutes=30)).strftime("%I:%M %p")), google_cal_id = google_cal_id, weekly=False)
        db.session.add(booking)
        db.session.commit() 

        flash("Booking sucessfully created", "success")
        
        return redirect(url_for("get_all_bookings", alternative_id = current_user.alternative_id))
    return redirect('/')

@app.route("/availability/<date>/<sitterid>/")
def get_available_times(date, sitterid):

    # sitterid = request.args.get('sitter_id')
    # date = request.args.get("start_date")
    # available_times = crud.get_available_times(date)

    free_times = gcalendar.free_times(selected_date=date, sitter_id = sitterid)
    # times_list = []
    # if free_time:
    #     for time in free_time:
    #         times_list.append(time)
    #         print("im the time", time)
    #         print("im all the free times", free_time)
    #     print("im the time_list", times_list)
    return free_times
    

        

    # free_time = gcalendar.free_times(selected_date=date, sitter_id = sitterid, selected_date = date)
    # print("im the free time on server", free_time)
    # return free_time



@app.route("/all_my_bookings/update/<booking_id>")
def update_event(booking_id):
    """update a booking"""
    
    if 'user_email' in session:

        current_user = crud.get_user_by_email(session['user_email'])
        booking = crud.get_booking_by_id(booking_id)
        google_booking_id = booking.google_booking_id
        cal_id = booking.sitter.user.email
        pet_owner_id = booking.pet_owner_id
        sitter_id = booking.pet_owner_id
        pet_id = booking.pet_id
        new_date = request.form.get("new_date")
        new_start_time = request.form.get("new_time")
        
        
        # info for creating the booking in google calendar
        new_address = request.form.get("address")
        new_description = request.form.get("description")

        # weekly = bool(request.form["weekly"])
        
        datetime_string = booking.new_date + "T" + new_start_time
        booking.start_date = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M")
        booking.end_date = (booking.start_date + timedelta(minutes=30))
        booking.start_time = booking.start_date.strftime("%I:%M %p")
        booking.end_time=((booking.start_date + timedelta(minutes=30)).strftime("%I:%M %p"))

        updated_event = gcalendar.update_booking(google_booking_id, cal_id)

        db.session.commit()

        flash("your booking was sucessfully updated")

        return redirect(url_for("get_all_bookings", alternative_id = current_user.alternative_id))
    return redirect('/')

    
@app.route('/search_availability/<alternative_id>', methods=["POST"])
@login_required
def display_available_sitters(alternative_id):
    """display sitters available on a specific time based on user search"""
    
    if 'user_email' in session:
            
        current_user = crud.get_user_by_alternative_id(alternative_id)
        # if request.method == 'GET':

        #     return redirect (url_for("all_sitters", alternative_id))
        
        available_sitters_email = gcalendar.get_available_sitters(alternative_id)
        if available_sitters_email == [] or not available_sitters_email:
            
            flash("There are no sitters available in the time you selected. Please try searching for a different time, or browing all the sitters in our database", "info")
            return redirect ('/')
        else:
            cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
            api_secret = API_SECRET)
        
            sitters=[]
            all_sitters = []
            for email in available_sitters_email:
                current_user = crud.get_user_by_email(email)
                available_sitter = crud.get_sitter_by_user_id(current_user.user_id)
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

            flash("These are the sitter available on the selected date and time")
            return render_template("all_sitters.html", sitters=sitters, current_user=current_user)

    return redirect('/')
            
    
@app.route('/sitters/<alternative_id>')
@login_required
def all_sitters(alternative_id):
    """View all sitters in db"""
    
    cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, 
    api_secret = API_SECRET)

    current_user = crud.get_user_by_alternative_id(alternative_id)
    all_sitters = crud.get_all_other_sitters(current_user.user_id)
    
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
@login_required
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
            

@app.route("/my_bookings/<alternative_id>")
@login_required
def get_all_bookings(alternative_id):
    """Return all the bookings made by a specific user"""
    
    sitter_bookings = False
    pet_owner_bookings = False

    if "user_email" in session: 
        
        current_user = crud.get_user_by_alternative_id(alternative_id)
        split_email = current_user.email.split("@")
        calendar_id = split_email[0]

        owner_bkngs = []
        if crud.petowner_exists(current_user.user_id):
            pet_owner_bookings = crud.get_owner_bookings_by_user_id(current_user.user_id)
            
            for booking in pet_owner_bookings:
            
                info_sitter={}
                info_sitter['booking_id'] = booking.id
                info_sitter['dog_name'] = booking.pet.name 
                info_sitter['sitter_pic'] = booking.sitter.user.profile_pic
                info_sitter['experience'] = booking.sitter.years_of_experience
                info_sitter ['summary'] = booking.sitter.summary
                info_sitter['date'] = booking.start_date.strftime("%m/%d/%Y")
                info_sitter['time'] = booking.start_time
                info_sitter['address'] = booking.pet_owner.user.address +", "+ booking.pet_owner.user.city +"-"+ booking.pet_owner.user.state
                info_sitter['sitter_name'] = booking.sitter.user.fname + " " + booking.sitter.user.lname
                info_sitter['sitter_mobile'] = booking.sitter.user.mobile
                info_sitter['sitter_email']  = booking.sitter.user.email
                info_sitter ['sitter_id'] = booking.sitter.id
                
                owner_bkngs.append(info_sitter)
                
        # check of sitter exists to then fetch sitters bookings, if  any.
        sitter_bkngs=[]
        if crud.sitter_exists(current_user.user_id):
            sitter_bookings = crud.get_sitter_bookings_by_user_id(current_user.user_id)
      
            
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
                info['time'] = booking.start_time
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
        return render_template("all_my_bookings.html", owner_bkngs=owner_bkngs, sitter_bkngs=sitter_bkngs, current_user = current_user, sitter_bookings = sitter_bookings, pet_owner_bookings = pet_owner_bookings)
    return redirect("/")


    return updated_event

@app.route("/logout")
@login_required
def logout():
    """remove the user from the session if it is there"""
    
    if 'user_email' in session:    
        remember = False
        session.pop('user_email', None)
        logout_user()
        print("you are now logged out", session['alternative_id'])
        
    return redirect('/')


@app.route("/delete/<user_id>")
@fresh_login_required
def confirm_delete_user(user_id):
    "Ask user to confirm if they want to delete their profile"
    
    user = crud.get_user_by_id(user_id)
    
    get_profile_page(user_id)
    
    
    return redirect(url_for("get_profile_page", user_id=user_id))
    
    
@app.route("/delete/<user_id>", methods=['POST'])
@fresh_login_required
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


