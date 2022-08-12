""" Script to seed the database"""

import os
from random import choice, randint
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


sitter1 = crud.create_sitter(fname="Michelle", lname= "James", email="michellej@test.com", password="J2wQsncNd7z5", profile_pic="profile_pic", years_of_experience=2, mobile="206-322-4980", address="709 Grand Street", zip_code=98136, rate=0.80)
sitter2 = crud.create_sitter(fname="Susan", lname= "Thomas", email="susant@test.com", password="ynBqMYf49VTa", profile_pic="profile_pic", years_of_experience=1, mobile="206-504-4397", address= "99 Kirkland Road", zip_code=98133, rate=0.90)
sitter3 = crud.create_sitter(fname="Brian", lname= "Sanchez", email="brians@test.com", password="Hr7XJyZYGTAC", profile_pic="profile_pic", years_of_experience=4, mobile="582-201-4225", address="709 Grand Street", zip_code=98118, rate=1.00)
sitter4 = crud.create_sitter(fname="Jared", lname= "Perkins", email="jaredp@test.com", password="LWTDNx2p8ZM9", profile_pic="profile_pic", years_of_experience=5, mobile="206-644-0852", address="8839 Sutor Drive", zip_code=98178, rate=0.75)


model.db.session.add_all([sitter1, sitter2, sitter3, sitter4])
model.db.session.commit()


pet_owner1 = crud.create_pet_owner(fname="Yesenia", lname="Orozco", email="yeseniao@test.com", password="2VM6E7rzTht8", profile_pic="profile_pic", num_pets=2, mobile="206-332-0913", address="9422 Buttonwood St", zip_code=98136, city='Seattle', state='Washington')    
pet_owner2 = crud.create_pet_owner(fname="Amanda", lname="Hays", email="amandah@test.com", password="uqh7X6pRWTYv", profile_pic="profile_pic", num_pets=1, mobile="206-144-0852", address="71 Anderson Lane", zip_code=98178, city='Seattle', state='Washington')    
pet_owner3 = crud.create_pet_owner(fname="Jason", lname="Jacobs", email="jasonj@test.com", password="djMtgQKsG6c8", profile_pic="profile_pic", num_pets=2, mobile="206-201-4225", address="40 Parker Ave", zip_code=98118, city='Seattle', state='Washington')    
pet_owner4 = crud.create_pet_owner(fname="Jose", lname="Guzman", email="joseg@test.com", password="3KM2NVU9HtbY", profile_pic="profile_pic", num_pets=1, mobile="315-444-4397", address="7669 Foxrun St.", zip_code=98133, city='Seattle', state='Washington')    

model.db.session.add_all([pet_owner1, pet_owner2, pet_owner3, pet_owner4])
model.db.session.commit()

pet1 = crud.create_pet(name="Bingo", profile_pic="profile_pic", breed="Labrador Retriver", age=2, size="large", allergies=False, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet2 = crud.create_pet(name="Benji", profile_pic="profile_pic", breed="Golden Retriver", age=3, size="large", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Maria", emergency_contact_relationship="mom", pet_owner_id=1)
pet3 = crud.create_pet(name="Lana", profile_pic="profile_pic", breed="Dobermann", age=5, size="large", allergies=True, allergies_kind="proteins", friendly_w_dogs=True, friendly_w_kids=False, spayed_neutered=True, microchipped=True, emergency_phone="206-778-4142", emergency_contact_name="Monica", emergency_contact_relationship="sister", pet_owner_id=2)
pet4 = crud.create_pet(name="Rocco", profile_pic="profile_pic", breed="Australian Cattle Dog", age=3, size="medium", allergies=True, allergies_kind="dairy", friendly_w_dogs=False, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone= "206-990-8082", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet5 = crud.create_pet(name="Tangles", profile_pic="profile_pic", breed="Poodle", age=2, size="medium", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Anthony", emergency_contact_relationship="partner", pet_owner_id=3)
pet6 = crud.create_pet(name="Brody", profile_pic="profile_pic", breed="Great Dane", age=4, size="giant", allergies=False, allergies_kind="n/a", friendly_w_dogs=True, friendly_w_kids=True, spayed_neutered=True, microchipped=True, emergency_phone="206-332-4980", emergency_contact_name="Jean", emergency_contact_relationship="partner", pet_owner_id=4)

model.db.session.add_all([pet1, pet2, pet3, pet4, pet5, pet6]) 
model.db.session.commit()      

vet1 = crud.create_vet(pet_id = 1, fname="Thomas", lname="Reid", mobile="206-444-3330", address="4 North Nichols St", zip_code="98133", city='Seattle', state='Washington')
vet2 = crud.create_vet(pet_id = 2, fname="Thomas", lname="Reid", mobile="206-444-3330", address="4 North Nichols St", zip_code="98133", city='Seattle', state='Washington')
vet3 = crud.create_vet(pet_id =3, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
vet4 = crud.create_vet(pet_id=4, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
vet5 = crud.create_vet(pet_id = 5, fname="Rodolfo", lname="Cortez", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
vet6 = crud.create_vet(pet_id = 6, fname="Luiz", lname="Souza", mobile="206-778-5050", address="4676 Roosevelt Wilson Lane", zip_code="98118", city='Seattle', state='Washington')
      
model.db.session.add_all([vet1, vet2, vet3, vet4, vet6]) 
model.db.session.commit()         


booking1 = crud.create_booking(weekly=False, pet=pet1, pet_owner=pet_owner1, sitter=sitter1)
booking2 = crud.create_booking(weekly=False, pet=pet2, pet_owner=pet_owner1, sitter=sitter1)
booking3 = crud.create_booking(weekly=False, pet=pet3, pet_owner=pet_owner2, sitter=sitter2)
booking4 = crud.create_booking(weekly=False, pet=pet4, pet_owner=pet_owner3, sitter=sitter3)
booking5 = crud.create_booking(weekly=False, pet=pet5, pet_owner=pet_owner3, sitter=sitter3)
booking6 = crud.create_booking(weekly=False, pet=pet6, pet_owner=pet_owner4, sitter=sitter4)

model.db.session.add_all([booking1, booking2, booking3, booking4, booking6]) 
model.db.session.commit() 