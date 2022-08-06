""" Script to seed the database"""

import os
import crud
import model
import server
from random import choice, randint
from datetime import datetime, timedelta

os.system('dropdb dog_walkers')
os.system('createdb dog_walkers')

model.connect_to_db(server.app)
model.db.create_all()

sitter_fnames = ["Michelle", "Susan", "Brian", "Carolyn", "Dawn" , "Jared", "Ashley", "Tammy", "Roy", "Daniel"]
sitter_lnames = ["James", "Thomas", "Sanchez", "Roach", "Perkins", "Snyder", "Holloway", "Clark", "Williams", "Benso"]
sitter_passwords = ["J2wQsncNd7z5", "Hr7XJyZYGTAC","WsXYLFeUf8yt","ynBqMYf49VTa", "LWTDNx2p8ZM9","Njpg6Hqzew2Z", "2mtrFvjqEYkQ", "gxFCLSc6HWYr", "ATsp53Gby8dJ","S8RJUcxVGBHN"]
sitter_mobile = ["206-322-4980", "206-644-9988", "317-451-6455", "206-628-4142", "582-200-8082", "206-652-5286", "206-300-0913", "206-504-4397", "582-201-4225", "206-644-0852"]
sitter_street =["709 Grand Street", "309 Snake Hill St","17 Sherman St", "7747 3rd St", "945 Miller Street", "13 Lilac Drive","8839 Sutor Drive", "38 North Street", "99 Kirkland Road","721 Roosevelt Street"]    ]
sitter_zip_code =[98136, 98133, 98122, 98101, 98161, 98108, 98117, 98178, 98146, 98118] 

pet_owner_fname = ["Yesenia","Kathryn", "Erica","Jason", "Tammy", "Monica", "Jason", "Emily" , "Anthony", "Tracy"]
pet_owner_lname = ["Orozco","Jacobs", "Jacobs","Howard", "Hays", " Brown", "Harris", "Armstrong"," Wilson", "Souza"]
owner_passwords = ["stSzWJa8T4RN","nYyLe9Gzdg5N", "2VM6E7rzTht8", "eHRa6wUByMru", "CfqKEWF6xpBL", "yrE7Czf2Ku9p", "uqh7X6pRWTYv", "djMtgQKsG6c8", "3KM2NVU9HtbY", "BpJRujE5ewLY"]
owner_mobile = ["206-332-4980", "206-644-1088", "206-451-5555", "206-778-4142", "206-990-8082", "414-652-5286", "206-332-0913", "315-444-4397", "206-201-4225", "206-144-0852"]
owner_street = ["734 Roosevelt Street", "84 Branch Road", "490 Bishop St", "4 North Nichols St", "72 Elizabeth Lane", "7669 Foxrun St.", "4 Pine Rd", "9422 Buttonwood St", "71 Anderson Lane", "40 Parker Ave"]
owner_zip_code = [98136, 98133, 98122, 98101, 98161, 98108, 98117, 98178, 98146, 98118]

vet_fname = ["Thomas", "Elaine", "Amanda", "Rodolfo", "Jose", "Maria", "Kyle" ]
vet_lname = ["Hall", "Everett", "Reid", "Pinilla", "Alcaraz","Guzman", "Lasta",]
vet_mobile = ["206-444-3330", "206-567-9870", "206-335-6098", "206-778-5050", "206-980-1092", "414-652-0974", "415-107-1930", "106-123-2097", "503-260-4225", "207-144-1652"]
vet_address = ["888 Union Street", "2200 Owagner Lane", "4676 Roosevelt Wilson Lane", "3018 Chipmunk Lane", "90 Owagner Lane", "9241 13th Ave SW", "9514 8th Ave S", "9668 Rainier Ave S"]  ]
vet_zip_code =[98133, 98122, 98101, 98161, 98108, 98106, 98118, 98136]

pet_names = ["Bingo", "Tangles", "Benji", "Skittles", "Wags","Lana", "Rocco", "Brody", "Cinnamon", "Ivy", "Layla", "Cocoa", "Boomer", "Cookie", "Biscuit"]

for n in range(10):
    random_fname=choice(sitter_fnames)
    random_lname=choice(sitter_lnames)
    email = f"{random_fname}@test.com"  # Voila! A unique email!
    random_password = choice(sitter_passwords)
    num_pets = randint(1,2)
    mobile = 

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)

