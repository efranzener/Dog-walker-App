""" Script to seed the database"""

import os
from random import choice, randint
from datetime import date
import datetime
import crud
import model
import server

# import datetime, timedelta
# from datetime import timedelta

os.system("dropdb dog_walkers --if-exists")
os.system("createdb dog_walkers")

model.connect_to_db(server.app)
print("connected to db")
model.db.create_all()


random_profile_pic = choice([x for x in os.listdir("templates/sitter pics") if os.path.isfile(os.path.join("templates/sitter pics", x))])



user1 = crud.create_user(fname="Michelle", lname= "James", dob= date.fromisoformat('2019-12-04'), email="michellej@test.com", password="J2wQsncNd7z5", profile_pic="profile_pic", mobile="206-322-4980", address="709 Grand Street", zip_code=98136, city='Seattle', state='Washington')
user2 = crud.create_user(fname="Susan", lname= "Thomas", dob= date.fromisoformat('2000-01-10'), email="susant@test.com", password="ynBqMYf49VTa", profile_pic="profile_pic",  mobile="206-504-4397", address= "99 Kirkland Road", zip_code=98133, city='Seattle', state='Washington')
user3 = crud.create_user(fname="Brian", lname= "Sanchez", dob= date.fromisoformat('1990-12-24'), email="brians@test.com", password="Hr7XJyZYGTAC", profile_pic="profile_pic",  mobile="582-201-4225", address="709 Grand Street", zip_code=98118, city='Seattle', state='Washington')
user4 = crud.create_user(fname="Jared", lname= "Perkins", dob= date.fromisoformat('1992-10-04'), email="jaredp@test.com", password="LWTDNx2p8ZM9", profile_pic="profile_pic",  mobile="206-644-0852", address="8839 Sutor Drive", zip_code=98178,city='Seattle', state='Washington')
user5 = crud.create_user(fname="Jose", lname="Guzman", dob= date.fromisoformat('1995-09-06'), email="joseg@test.com", password="3KM2NVU9HtbY" ,profile_pic="profile_pic", mobile="206-144-0852", address="71 Anderson Lane", zip_code=98178, city='Seattle', state='Washington')
user6 = crud.create_user(fname="Mario", lname="Rodrigues", dob= date.fromisoformat('1999-11-06'), email="marior@test.com", password="9KjhmNHtbY", profile_pic="profile_pic", mobile="206-164-9870", address="777 Anderson Street", zip_code=98133, city='Seattle', state='Washington')


model.db.session.add_all([user1, user2, user3, user4, user5, user6])
model.db.session.commit()

sitter1 = crud.create_sitter(user_id = 1, years_of_experience=2,  summary="summary", rate=20.00)
sitter2 = crud.create_sitter(user_id = 2, years_of_experience=2,  summary="summary", rate=30.00)
sitter3 = crud.create_sitter(user_id = 3, years_of_experience=2,  summary="summary", rate=25.00)


model.db.session.add_all([sitter1, sitter2, sitter3])
model.db.session.commit()


pet_owner1 = crud.create_pet_owner(user_id = 4, num_pets=2)    
pet_owner2 = crud.create_pet_owner(user_id = 5, num_pets=1)   
pet_owner3 = crud.create_pet_owner(user_id = 6, num_pets=2)    

model.db.session.add_all([pet_owner1, pet_owner2, pet_owner3])
model.db.session.commit()

pet1 = crud.create_pet(name="Bingo", profile_pic="profile_pic", breed="Labrador Retriver", age=2, size="large", allergies=False, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet2 = crud.create_pet(name="Benji", profile_pic="profile_pic", breed="Golden Retriver", age=3, size="large", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet3 = crud.create_pet(name="Lana", profile_pic="profile_pic", breed="Dobermann", age=5, size="large", allergies=True, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=False, spayed_neutered=True, microchipped=True, emergency_phone="206-778-4142", emergency_contact_name="Monica", emergency_contact_relationship="sister", pet_owner_id=2)
pet4 = crud.create_pet(name="Rocco", profile_pic="profile_pic", breed="Australian Cattle Dog", age=3, size="medium", allergies=True, allergies_kind="dairy", friendly_w_dogs=False, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone= "206-990-8082", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet5 = crud.create_pet(name="Tangles", profile_pic="profile_pic", breed="Poodle", age=2, size="medium", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet6 = crud.create_pet(name="Brody", profile_pic="profile_pic", breed="Great Dane", age=4, size="giant", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Jean", emergency_contact_relationship="partner", pet_owner_id=4)

model.db.session.add_all([pet1, pet2, pet3, pet4, pet5, pet6]) 
model.db.session.commit()      

# vet1 = crud.create_vet(pet_id = 1, fname="Thomas", lname="Reid", mobile="206-444-3330", address="4 North Nichols St", zip_code="98133", city='Seattle', state='Washington')
# vet2 = crud.create_vet(pet_id = 2, fname="Thomas", lname="Reid", mobile="206-444-3330", address="4 North Nichols St", zip_code="98133", city='Seattle', state='Washington')
# vet3 = crud.create_vet(pet_id =3, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
# vet4 = crud.create_vet(pet_id=4, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
# vet5 = crud.create_vet(pet_id = 5, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
# vet6 = crud.create_vet(pet_id = 6, fname="Luiz", lname="Souza", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
      
# model.db.session.add_all([vet1, vet2, vet3, vet4, vet6]) 
# model.db.session.commit()         


# booking1 = crud.create_booking(weekly=False, pet=pet1, pet_owner=pet_owner1, sitter=sitter1)
# booking2 = crud.create_booking(weekly=False, pet=pet2, pet_owner=pet_owner1, sitter=sitter1)
# booking3 = crud.create_booking(weekly=False, pet=pet3, pet_owner=pet_owner2, sitter=sitter2)
# booking4 = crud.create_booking(weekly=False, pet=pet4, pet_owner=pet_owner3, sitter=sitter3)
# booking5 = crud.create_booking(weekly=False, pet=pet5, pet_owner=pet_owner3, sitter=sitter3)
# booking6 = crud.create_booking(weekly=False, pet=pet6, pet_owner=pet_owner4, sitter=sitter4)

# model.db.session.add_all([booking1, booking2, booking3, booking4, booking6]) 
# model.db.session.commit() 