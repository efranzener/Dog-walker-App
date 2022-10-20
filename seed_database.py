""" Script to seed the database"""

import os
from datetime import date, timedelta, time
import datetime
import crud
import model
import server
from werkzeug.utils import secure_filename
import uuid as uuid


from flask_bcrypt import generate_password_hash


# from model import db, User, Sitter, PetOwner, Pet, Vet, Booking, connect_to_db
from random import random, randrange
from datetime import timedelta, datetime
import datetime as dt


# CLOUDINARY IMPORT
import cloudinary
import cloudinary.uploader
import cloudinary.api

# import os.path
import flask

os.system("dropdb dog_walkers")
os.system("createdb dog_walkers")

model.connect_to_db(server.app)
model.db.create_all()

cloud_config = cloudinary.config(secure=True)
API_KEY = os.environ['cloudinary_api_key']
API_SECRET = os.environ['api_secret']
CLOUD_NAME = os.environ['cloud_name']


# def create_profile_pic():
#     """create a standard profile picture uploading it to claudinary"""
    
#     cloudinary.config(cloud_name = CLOUD_NAME, api_key = API_KEY, api_secret = API_SECRET)
#     upload_result = cloudinary.uploader.upload("static/usericon.jpg", folder = "static")

#     data = upload_result
#     img = data['url']

#     return img 

# img=create_profile_pic()


poodle = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663619848/poodle_qodkol.jpg'
lab_retriever = 'https://res.cloudinary.com/dggbnnudv/image/upload/v1664943624/noemi-macavei-katocz-c7bUIRBqapA-unsplash_hnejhd.jpg'
golden_retriever = "https://res.cloudinary.com/dggbnnudv/image/upload/v1664991360/jacob-thorson-fFYBRyC_OAk-unsplash_lenvse.jpg"
blue_heeler = 'https://res.cloudinary.com/dggbnnudv/image/upload/v1664943175/daniel-lincoln-E7E8z3OWNf4-unsplash_dfjawk.jpg'
great_dane = 'https://res.cloudinary.com/dggbnnudv/image/upload/v1664943482/chris-mcintosh-DBrgUcBG_rg-unsplash_xcg21t.jpg'


user1 = crud.create_user(fname="Michelle", lname= "James", dob= date.fromisoformat('1995-12-04'), email="testuser.numone@gmail.com", password=generate_password_hash("QWERTyuiop1?", rounds=12).decode("utf-8"), profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664942203/i7kboife9afigqzcildi.jpg", mobile="206-322-4980", address="8016 Greenwood Ave N", zip_code= 98103, city='Seattle', state='Washington', authenticated=False)
user2 = crud.create_user(fname="Susan", lname= "Thomas", dob= date.fromisoformat('2000-01-10'), email="testuser.numtwo@gmail.com", password=generate_password_hash("ASDFGhjkl2?").decode("utf-8"), profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664991252/jorge-salvador-Y6GZ97S-mcY-unsplash_o8ok6z.jpg",  mobile="206-504-4397", address= "2801 34th Ave W", zip_code=98199, city='Seattle', state='Washington', authenticated=False)
user3 = crud.create_user(fname="Brian", lname= "Sanchez", dob= date.fromisoformat('1990-12-24'), email="testuser.numthree@gmail.com", password=generate_password_hash("ZXCVBnm3?").decode("utf-8"), profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664991758/tadeusz-lakota-tk5LWGNiWVs-unsplash_r94szu.jpg",  mobile="582-201-4225", address="1501 N 45th St", zip_code=98103, city='Seattle', state='Washington', authenticated=False)
user4 = crud.create_user(fname="Kate", lname= "Perkins", dob= date.fromisoformat('1992-10-04'), email="testuser.numfour@gmail.com", password=generate_password_hash("ZXCVBnm4?").decode("utf-8"),  profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664991573/isaiah-mcclean-DrVJk1EaPSc-unsplash_qjhttx.jpg",  mobile="206-644-0852", address="5614, 22nd Ave NW", zip_code=98107,city='Seattle', state='Washington', authenticated=False)


sitter1 = crud.create_sitter(user_id = 1, years_of_experience=5,  summary="I'm a pet sitter with many years of experience. I'm currently working as a part-time sitter and a part-time caregiver for an elderly couple. On my free time I enjoy spending time with my own pups and panting.", rate=20.00)
sitter2 = crud.create_sitter(user_id = 2, years_of_experience=4,  summary="I'm a full time dog walker, and I love my job. I'm currently looking to add a few more pups to my regular schedule. Please feel free to send me a booking request if you are looking for a regular dog walker.", rate=30.00)
sitter3 = crud.create_sitter(user_id = 3, years_of_experience=2,  summary="Hello! I have just joined this platform and although I don't have a lot of experience as a professional dog walkers, I have extensive experience informally pet sitting and deg walking my friend's pets. Please feel free to reach out if you would like to book a walk with me or would like to ask any questions prior to that. ", rate=25.00)


pet_owner1 = crud.create_pet_owner(user_id = 1, num_pets=2)    
pet_owner2 = crud.create_pet_owner(user_id = 2, num_pets=1)   
pet_owner3 = crud.create_pet_owner(user_id = 3, num_pets=2)    
pet_owner4 = crud.create_pet_owner(user_id = 4, num_pets=1)    


pet1 = crud.create_pet(name="Bingo", profile_pic=lab_retriever, breed="Labrador Retriver", age=2, size="large", allergies=False, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet2 = crud.create_pet(name="Benji", profile_pic=golden_retriever, breed="Golden Retriver", age=3, size="large", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet3 = crud.create_pet(name="Lana", profile_pic=great_dane, breed="Great Dane", age=5, size="giant", allergies=True, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=False, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-778-4142", emergency_contact_name="Monica", emergency_contact_relationship="sister", pet_owner_id=2)
pet4 = crud.create_pet(name="Rocco", profile_pic=blue_heeler, breed="Australian Cattle Dog", age=3, size="medium", allergies=True, allergies_kind="dairy", friendly_w_dogs=False, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone= "206-990-8082", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet5 = crud.create_pet(name="Tangles", profile_pic=poodle, breed="Poodle", age=2, size="small", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
   


now = datetime.now()
local_time = time(now.hour, now.minute, now.second)
date_today = datetime.today().strftime("%Y-%m-%d")
date_end = (datetime.today() + timedelta(days=60)).strftime("%Y-%m-%d")
start_today = datetime.strptime(date_today, "%Y-%m-%d")
end_date = datetime.strptime(date_end, "%Y-%m-%d")

max_time = time(hour=23, minute=00, second=00)
min_time = time(hour=6, minute=00, second=00)

def creating_datetimes(start_today, end_date):
    """ Return a random datetime"""
    
    interval_dates = (end_date - start_today)
    interval = (interval_dates.days * 24 * 60 * 60)
    random_date = randrange(interval)
    random_datetime = start_today + timedelta(seconds=random_date)

    if random_datetime.minute > 0:
        random_datetime = random_datetime + (datetime.min - random_datetime) % timedelta(minutes=60)
        
   
    if random_datetime.date() == start_today:
        while (random_datetime.time() > max_time and random_datetime.time() < local_time):
            random_date = randrange(interval)
            random_datetime = start_today + timedelta(seconds=random_date)
            random_datetime = random_datetime + (datetime.min - random_datetime) % timedelta(minutes=60)
    else:
        while (random_datetime.time() < min_time and random_datetime.time() > max_time):
            random_date = randrange(interval)
            random_datetime = start_today + timedelta(seconds=random_date)
            random_datetime = random_datetime + (datetime.min - random_datetime) % timedelta(minutes=60)
    random_datetime= random_datetime

    return random_datetime

  
start_date = creating_datetimes(start_today, end_date)
start_time = start_date
end_time = (start_date + timedelta(minutes=30)) 
    
booking1 = crud.create_booking(weekly=False, pet_id=pet1.pet_id, pet_owner_id=3, sitter_id=1,  start_date=start_date, end_date=start_date, start_time=start_time, end_time=end_time)
start_date = creating_datetimes(start_today, end_date)
end_time = (start_date + timedelta(minutes=30))  

booking2 = crud.create_booking(weekly=False, pet_id=pet2.pet_id, pet_owner_id=1, sitter_id=2,  start_date=start_date, end_date=start_date, start_time=start_time, end_time=end_time)
start_date = creating_datetimes(start_today, end_date)
end_time = (start_date + timedelta(minutes=30))  

booking3 = crud.create_booking(weekly=False, pet_id=pet3.pet_id, pet_owner_id=2, sitter_id=3,  start_date=start_date, end_date=start_date, start_time=start_time, end_time=end_time)
start_date = creating_datetimes(start_today, end_date)
end_time = (start_date + timedelta(minutes=30))  

booking4 = crud.create_booking(weekly=False, pet_id=pet4.pet_id, pet_owner_id=4, sitter_id=1,  start_date=start_date, end_date=start_date, start_time=start_time, end_time=end_time)
start_date = creating_datetimes(start_today, end_date)
end_time = (start_date + timedelta(minutes=30))  

booking5 = crud.create_booking(weekly=False, pet_id=pet5.pet_id, pet_owner_id=1, sitter_id=2,  start_date=start_date, end_date=start_date, start_time=start_time, end_time=end_time)
start_date = creating_datetimes(start_today, end_date)
end_time = (start_date + timedelta(minutes=30))  

booking6 = crud.create_booking(weekly=False, pet_id=pet3.pet_id, pet_owner_id=4, sitter_id=3,  start_date=start_date, end_date=start_date, start_time=start_time, end_time=end_time)

    
model.db.session.add_all([booking1, booking2, booking3, booking4, booking6]) 
model.db.session.commit() 


if __name__ == "__main__":
    from server import app