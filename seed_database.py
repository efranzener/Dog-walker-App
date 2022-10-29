""" Script to seed the database"""

import os
from datetime import date, timedelta, time
import datetime
import crud
import model
import server
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeSerializer

from flask_bcrypt import generate_password_hash


from model import db
import random
from datetime import timedelta, datetime
import datetime as dt


# # CLOUDINARY IMPORT
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# import os.path
import flask

os.system("dropdb dog_walkers")
os.system("createdb dog_walkers")

model.connect_to_db(server.app)
model.db.create_all()
secret_key = os.environ['secret_key']
serializer = URLSafeSerializer(server.app.secret_key)

# cloud_config = cloudinary.config(secure=True)
# API_KEY = os.environ['cloudinary_api_key']
# API_SECRET = os.environ['api_secret']
# CLOUD_NAME = os.environ['cloud_name']


poodle = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663619848/poodle_qodkol.jpg'
lab_retriever = 'https://res.cloudinary.com/dggbnnudv/image/upload/v1664943624/noemi-macavei-katocz-c7bUIRBqapA-unsplash_hnejhd.jpg'
golden_retriever = "https://res.cloudinary.com/dggbnnudv/image/upload/v1664991360/jacob-thorson-fFYBRyC_OAk-unsplash_lenvse.jpg"
blue_heeler = 'https://res.cloudinary.com/dggbnnudv/image/upload/v1664943175/daniel-lincoln-E7E8z3OWNf4-unsplash_dfjawk.jpg'
great_dane = 'https://res.cloudinary.com/dggbnnudv/image/upload/v1664943482/chris-mcintosh-DBrgUcBG_rg-unsplash_xcg21t.jpg'

password="QWERTyuiop1?"
user1 = crud.create_user(fname="Michelle", lname="James", dob=date.fromisoformat('1995-12-04'), email ="testuser.numone@gmail.com", password=generate_password_hash(password, rounds=12).decode("utf-8"), alternative_id = serializer.dumps(["testuser.numone@gmail.com", password]),
                         profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664942203/i7kboife9afigqzcildi.jpg", mobile="206-322-4980", address="8016 Greenwood Ave N", zip_code=98103, city='Seattle', state='Washington', authenticated=False)
password = "ASDFGhjkl2?"
user2 = crud.create_user(fname="Susan", lname="Thomas", dob=date.fromisoformat('2000-01-10'), email="testuser.numtwo@gmail.com", password=generate_password_hash(password).decode("utf-8"), alternative_id = serializer.dumps(["testuser.numtwo@gmail.com", password]),
                         profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664991252/jorge-salvador-Y6GZ97S-mcY-unsplash_o8ok6z.jpg",  mobile="206-504-4397", address="2801 34th Ave W", zip_code=98199, city='Seattle', state='Washington', authenticated=False)
password = "ZXCVBHjn?nm3?"
user3 = crud.create_user(fname="Brian", lname="Sanchez", dob=date.fromisoformat('1990-12-24'), email="testuser.numthree@gmail.com", password=generate_password_hash(password).decode("utf-8"), alternative_id = serializer.dumps(["testuser.numthree@gmail.com", password]),
                         profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664991758/tadeusz-lakota-tk5LWGNiWVs-unsplash_r94szu.jpg",  mobile="582-201-4225", address="1501 N 45th St", zip_code=98103, city='Seattle', state='Washington', authenticated=False)
password = "ZXCVGbk!nm4?"
user4 = crud.create_user(fname="Kate", lname="Perkins", dob=date.fromisoformat('1992-10-04'), email="testuser.numfour@gmail.com", password=generate_password_hash(password).decode("utf-8"), alternative_id = serializer.dumps(["testuser.numfour@gmail.com", password]),
                         profile_pic="https://res.cloudinary.com/dggbnnudv/image/upload/v1664991573/isaiah-mcclean-DrVJk1EaPSc-unsplash_qjhttx.jpg",  mobile="206-644-0852", address="5614, 22nd Ave NW", zip_code=98107, city='Seattle', state='Washington', authenticated=False)

db.session.add_all([user1, user2, user3, user4])

db.session.commit()

sitter1 = crud.create_sitter(user_id=1, years_of_experience=5,
                             summary="I'm a pet sitter with many years of experience. I'm currently working as a part-time sitter and a part-time caregiver for an elderly couple. On my free time I enjoy spending time with my own pups and panting.", rate=20.00)
sitter2 = crud.create_sitter(user_id=2, years_of_experience=4,
                             summary="I'm a full time dog walker, and I love my job. I'm currently looking to add a few more pups to my regular schedule. Please feel free to send me a booking request if you are looking for a regular dog walker.", rate=30.00)
sitter3 = crud.create_sitter(user_id=3, years_of_experience=2,  summary="Hello! I have just joined this platform and although I don't have a lot of experience as a professional dog walkers, I have extensive experience informally pet sitting and deg walking my friend's pets. Please feel free to reach out if you would like to book a walk with me or would like to ask any questions prior to that. ", rate=25.00)
db.session.add_all([sitter1, sitter2, sitter3])
db.session.commit()

pet_owner1 = crud.create_pet_owner(user_id=1, num_pets=2)
pet_owner2 = crud.create_pet_owner(user_id=2, num_pets=1)
pet_owner3 = crud.create_pet_owner(user_id=3, num_pets=2)
pet_owner4 = crud.create_pet_owner(user_id=4, num_pets=1)
db.session.add_all([pet_owner1, pet_owner2, pet_owner3, pet_owner4])
db.session.commit()

pet1 = crud.create_pet(name="Bingo", profile_pic=lab_retriever, breed="Labrador Retriver", age=2, size="large", allergies=False, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=True,
                       spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet2 = crud.create_pet(name="Benji", profile_pic=golden_retriever, breed="Golden Retriver", age=3, size="large", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True,
                       microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet3 = crud.create_pet(name="Lana", profile_pic=great_dane, breed="Great Dane", age=5, size="giant", allergies=True, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=False, spayed_neutered=True,
                       microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-778-4142", emergency_contact_name="Monica", emergency_contact_relationship="sister", pet_owner_id=2)
pet4 = crud.create_pet(name="Rocco", profile_pic=blue_heeler, breed="Australian Cattle Dog", age=3, size="medium", allergies=True, allergies_kind="dairy", friendly_w_dogs=False, friendly_w_kids=True, spayed_neutered=True,
                       microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-990-8082", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet5 = crud.create_pet(name="Tangles", profile_pic=poodle, breed="Poodle", age=2, size="small", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True,
                       microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
db.session.add_all([pet1, pet2, pet3, pet4, pet5])
db.session.commit()


start = datetime.now() + timedelta(days=1)
end = datetime.now() + timedelta(days=30)


def create_random_datetime(start, end):
    """pick a random datetime"""

    interval_days = end - start
    random_number = random.randrange(interval_days.days * 24 * 60 * 60)

    random_datetime = start + timedelta(seconds=random_number)

    # check if random datetime is in the hour or hours and half mark, and if not it rounds it to be
    if random_datetime.minute > 0:

        random_datetime = random_datetime + \
            (datetime.min - random_datetime) % timedelta(minutes=30)

    return random_datetime


date = create_random_datetime(start, end)
time_string = date.strftime("%I:%M %p")


def create_booking():
    """create sample bookings"""

    for n in range(1, 4):

        pet_owner = crud.get_petowner_by_user_id(n)
        sitters = crud.get_all_other_sitters(n)
        pets = crud.get_pets_by_ownerid(pet_owner.id)

        for sitter in sitters:
            for pet in pets:
                date = create_random_datetime(start, end)
                time_string = date.strftime("%I:%M %p")

                if crud.check_availability_by_datetime(date, time_string):
                    date = create_random_datetime(start, end)
                    time_string = date.strftime("%I:%M %p")

                booking = crud.create_booking(weekly=False, pet_id=pet.pet_id, pet_owner_id=pet_owner.id,
                                              sitter_id=sitter.id,  start_date=date, end_date=date + timedelta(minutes=30), start_time=time_string, end_time=(date + timedelta(minutes=30)).strftime("%I:%M %p"))
                model.db.session.add(booking)
                model.db.session.commit()
                print("Im a new booking", booking)


create_booking()


if __name__ == "__main__":
    from server import app
