""" Script to seed the database"""

import os
from random import choice, randint
from datetime import date
import datetime
import crud
import model
import server
# 

# import datetime, timedelta
# from datetime import timedelta

os.system("dropdb dog_walkers --if-exists")
print("database dog walkers dropped")
os.system("createdb dog_walkers")

model.connect_to_db(server.app)
print("connected to db")
model.db.create_all()


img = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663618707/default-avatar-profile-icon-vector-39013212_kxljdk.jpg'
poodle = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663619848/poodle_qodkol.jpg'
lab_retriever = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663619848/f34ad5352f6b21dd88a6749812d341d7--chocolate-labrador-retriever-chocolate-labradors_qwpzml.jpg'
golden_retriever = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663619848/golden-retriever-dog-breed-info_hltdjo.jpg'
blue_heeler = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663619850/Screen_Shot_2016-02-09_at_6.56.59_PM_fpj2zl.png'
great_dane = 'https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663620387/great_dane_d4hbpm.jpg'

user1 = crud.create_user(fname="Michelle", lname= "James", dob= date.fromisoformat('1995-12-04'), email="testuser.numone@gmail.com", password="QWERTyuiop1?", profile_pic=img, mobile="206-322-4980", address="8016 Greenwood Ave N", zip_code= 98103, city='Seattle', state='Washington')
user2 = crud.create_user(fname="Susan", lname= "Thomas", dob= date.fromisoformat('2000-01-10'), email="testuser.numtwo@gmail.com", password="ASDFGhjkl2?", profile_pic=img,  mobile="206-504-4397", address= "2801 34th Ave W", zip_code=98199, city='Seattle', state='Washington')
user3 = crud.create_user(fname="Brian", lname= "Sanchez", dob= date.fromisoformat('1990-12-24'), email="testuser.numthree@gmail.com", password="ZXCVBnm3?", profile_pic=img,  mobile="582-201-4225", address="1501 N 45th St", zip_code=98103, city='Seattle', state='Washington')
user4 = crud.create_user(fname="Jared", lname= "Perkins", dob= date.fromisoformat('1992-10-04'), email="testuser.numfour@gmail.com", password="ZXCVBnm4?", profile_pic=img,  mobile="206-644-0852", address="5614, 22nd Ave NW", zip_code=98107,city='Seattle', state='Washington')
# user5 = crud.create_user(fname="Jose", lname="Guzman", dob= date.fromisoformat('1995-09-06'), email="joseg@test.com", password="3KM2NVU9HtbY" ,profile_pic="profile_pic", mobile="206-144-0852", address="71 Anderson Lane", zip_code=98178, city='Seattle', state='Washington')
# user6 = crud.create_user(fname="Mario", lname="Rodrigues", dob= date.fromisoformat('1999-11-06'), email="marior@test.com", password="9KjhmNHtbY", profile_pic="profile_pic", mobile="206-164-9870", address="777 Anderson Street", zip_code=98133, city='Seattle', state='Washington')




model.db.session.add_all([user1, user2, user3, user4])
model.db.session.commit()

sitter1 = crud.create_sitter(user_id = 1, years_of_experience=5,  summary="I'm a pet sitter with many years of experience. I'm currently working as a part-time sitter and a part-time caregiver for an elderly couple. On my free time I enjoy spending time with my own pups and panting.", rate=20.00)
sitter2 = crud.create_sitter(user_id = 2, years_of_experience=4,  summary="I'm a full time dog walker, and I love my job. I'm currently looking to add a few more pups to my regular schedule. Please feel free to send me a booking request if you are looking for a regular dog walker.", rate=30.00)
sitter3 = crud.create_sitter(user_id = 3, years_of_experience=2,  summary="Hello! I have just joined this platform and although I don't have a lot of experience as a professional dog walkers, I have extensive experience informally pet sitting and deg walking my friend's pets. Please feel free to reach out if you would like to book a walk with me or would like to ask any questions prior to that. ", rate=25.00)


model.db.session.add_all([sitter1, sitter2, sitter3])
model.db.session.commit()


pet_owner1 = crud.create_pet_owner(user_id = 1, num_pets=2)    
pet_owner2 = crud.create_pet_owner(user_id = 2, num_pets=1)   
pet_owner3 = crud.create_pet_owner(user_id = 3, num_pets=2)    
pet_owner4 = crud.create_pet_owner(user_id = 4, num_pets=1)    

model.db.session.add_all([pet_owner1, pet_owner2, pet_owner3])
model.db.session.commit()

pet1 = crud.create_pet(name="Bingo", profile_pic=lab_retriever, breed="Labrador Retriver", age=2, size="large", allergies=False, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet2 = crud.create_pet(name="Benji", profile_pic=golden_retriever, breed="Golden Retriver", age=3, size="large", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet3 = crud.create_pet(name="Lana", profile_pic=great_dane, breed="Great Dane", age=5, size="giant", allergies=True, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=False, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-778-4142", emergency_contact_name="Monica", emergency_contact_relationship="sister", pet_owner_id=2)
pet4 = crud.create_pet(name="Rocco", profile_pic=blue_heeler, breed="Australian Cattle Dog", age=3, size="medium", allergies=True, allergies_kind="dairy", friendly_w_dogs=False, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone= "206-990-8082", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet5 = crud.create_pet(name="Tangles", profile_pic=poodle, breed="Poodle", age=2, size="small", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, house_trained=True, additional_info="Nothing to add", emergency_phone="206-332-4980", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)

model.db.session.add_all([pet1, pet2, pet3, pet4, pet5]) 
model.db.session.commit()      

# vet1 = crud.create_vet(pet_id = 1, fname="Thomas", lname="Reid", mobile="206-444-3330", address="4 North Nichols St", zip_code="98133", city='Seattle', state='Washington')
# vet2 = crud.create_vet(pet_id = 2, fname="Thomas", lname="Reid", mobile="206-444-3330", address="4 North Nichols St", zip_code="98133", city='Seattle', state='Washington')
# vet3 = crud.create_vet(pet_id =3, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
# vet4 = crud.create_vet(pet_id=4, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
# vet5 = crud.create_vet(pet_id = 5, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
      
# model.db.session.add_all([vet1, vet2, vet3, vet4]) 
# model.db.session.commit()         


# booking1 = crud.create_booking(weekly=False, pet=pet1, pet_owner=pet_owner1, sitter=sitter1)
# booking2 = crud.create_booking(weekly=False, pet=pet2, pet_owner=pet_owner1, sitter=sitter1)
# booking3 = crud.create_booking(weekly=False, pet=pet3, pet_owner=pet_owner2, sitter=sitter2)
# booking4 = crud.create_booking(weekly=False, pet=pet4, pet_owner=pet_owner3, sitter=sitter3)
# booking5 = crud.create_booking(weekly=False, pet=pet5, pet_owner=pet_owner3, sitter=sitter3)
# booking6 = crud.create_booking(weekly=False, pet=pet3, pet_owner=pet_owner2, sitter=sitter3)

# model.db.session.add_all([booking1, booking2, booking3, booking4, booking6]) 
# model.db.session.commit() 