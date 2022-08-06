"""Models for dog walker app"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timedelta
import os

app = Flask(__name__)
db = SQLAlchemy()


class Sitter(db.Model):
    """ A pet sitter"""

    __tablename__ = 'sitters'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable = False)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    profile_pic = db.Column(db.String(300), nullable = False)
    summary = db.Column (db.Text)
    years_of_experience = db.Column(db.Integer, nullable=False)
    mobile = db.Column(db.String(15), nullable = False)
    street_address = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(20), nullable = False)
    zip_code = db.Column(db.String(5), nullable = False)
    minute_rate = db.Column(db.Float, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # bookings = a list of Booking objects


def __repr__(self):
    """Show info about sitter"""

    return f'<Sitter id = {self.id}, email={self.email}, password={self.password}, fname = {self.first_name}, lname = {self.last_name}, profile_pic = {self.profile_pic}, summary = {self.summary}, experience = {self.years_of_experience}, mobile = {self.mobile}, street_address = {self.street_address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}, minute_rate = {self.minute_rate}>'


class PetOwner(db.Model):
    """A pet's owner info"""

    __tablename__ = "pet_owners"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable = False)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    profile_pic = db.Column(db.String(300), nullable = False)
    num_pets = db.Column(db.Integer)
    mobile = db.Column(db.String(15), nullable = False)
    street_address = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(20), nullable = False)
    zip_code = db.Column(db.String(5), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # bookings = a list of Booking objects
    
    pets = db.relationship('Pet', backref = "pet_owner")


def __repr__(self):
    """Show info about pet owner"""

    return f"<PetOwner id={self.id}, email={self.email}, password={self.password}, fname = {self.first_name}, lname = {self.last_name}, profile_pic = {self.profile_pic}, num_pets = {self.num_pets}, mobile = {self.mobile}, street_address = {self.street_address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}>"
    

class Pet(db.Model):
    """A pet info"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    profile_pic = db.Column(db.String(300), nullable = False)
    breed = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    size = db.Column(db.String(100), nullable = False)
    allergies = db.Column(db.Boolean, default=False, nullable = False)
    allergies_kind = db.Column(db.String(100))
    house_trained = db.Column(db.Boolean)
    friendly_w_dogs = db.Column(db.Boolean, default=False, nullable = False)
    friendly_w_kids = db.Column(db.Boolean, default=False, nullable = False)
    spayed_neutered = db.Column(db.Boolean, default=False, nullable = False)
    microchipped = db.Column(db.Boolean, default=False, nullable = False)
    additional_info = db.Column(db.Text)
    pet_owner_id = db.Column(db.Integer, db.ForeignKey("pet_owners.id"))
    emergency_phone = db.Column(db.String(15), nullable = False)
    emergency_contact_name = db.Column(db.String(100), nullable = False)
    emergency_contact_relationship = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # bookings = a list of Booking objects


def __repr__(self):
    """Show info about pet"""

    return f"<Pet id ={self.id}, name = {self.name}, profile_pic = {self.profile_pic}, breed = {self.breed}, age = {self.age}, size = {self.age}, allergies = {self.allergies}, friendly_w_dogs = {self.friendly_w_dogs}, friendly_w_kids = {self.friendly_w_kids}, spayed_neutured = {self.spayed_neutered}, microchipped = {self.microchipped}, emergency_phone = {self.emergency_phone}, emergency_contact_name = {self.emergency_contact_name}, emergency_contact_relationship = {self.emergency_contact_relationship}>"


class Vet(db.Model):
    """A pet's vet info"""

    __tablename__ = "vets"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"))
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    mobile = db.Column(db.String(15), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(20), nullable = False)
    zip_code = db.Column(db.String(5), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    pets = db.relationship("Pet", backref = 'vet')


def __repr__(self):
    """Show info about Vet"""

    return f"<Vet id ={self.id}, first_name = {self.first_name}, last_name = {self.last_name}, mobile = {self.mobile}, street_address = {self.street_address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}>"
    

class Booking(db.Model):
    """A booking info"""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pet_owner_id = db.Column(db.Integer, db.ForeignKey("pet_owners.id"))
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.id"))
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"))
    start_date = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    end_date = db.Column(db.DateTime, default=datetime.now() + timedelta(days=180), nullable = False)
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    end_time = db.Column(db.DateTime, default=datetime.now() + timedelta(hours=24), nullable = False)
    weekly = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    pet = db.relationship("Pet", backref = 'bookings')
    sitter = db.relationship("Sitter", backref = 'bookings')
    pet_owner = db.relationship("PetOwner", backref = 'bookings')


def __repr__(self):
    """Show info about booking"""

    return f"<Booking id ={self.id}, start_date = {self.start_date}, end_date = {self.end_date}, start_time = {self.start_time}, end_time = {self.end_time}>"


def connect_to_db(app, db_uri="postgresql:///dog_walkers", echo=True):
    """Connect to database."""

    # os.system("dropdb dog_walker --if-exists")
    # os.system("createdb dog_walker")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    # db.create_all()
    print("Connected to the db!")

    # test_sitter1 = Sitter(email = 'test@test.com', password = 'test', fname = 'Test', lname = 'testing', profile_pic = 'jpeg', summary = "hello, I'm just a test", years_of_experience = 2, mobile = 0000000000, street_address = 'Test Street', city = 'Seatest', state = 'Washington', zip_code = 98124, minute_rate = 0.80)
    # test_owner1 = PetOwner(email = 'owner@pets.com', password = 'owner_test', fname = 'Owner', lname = 'smith', profile_pic = 'jpeg', num_pets=2, mobile = 100000000, street_address = 'Test Street owner', city = 'Seatest', state = 'Washington', zip_code = 98124)
    # test_pet1 = Pet(name = 'cookie', profile_pic = 'jpeg', breed = 'pitbull', age = 3, size = 'medium', allergies = True, friendly_w_dogs = True, friendly_w_kids = True, spayed_neutered = True, microchipped = True, pet_owner_id = 1, emergency_phone = 333333333, emergency_contact_name = 'Aline', emergency_contact_relationship = 'Uncle')
    # test_booking1 = Booking(pet_owner_id = 1,  sitter_id = 1, pet_id = 1, weekly=True)

    # test_pet2 = Pet(name = 'Peanut', profile_pic = 'jpeg', breed = 'lab', age = 2, size = 'medium', allergies = False, friendly_w_dogs = True, friendly_w_kids = True, spayed_neutered = True, microchipped = True, pet_owner_id = 1, emergency_phone = 333333333, emergency_contact_name = 'Aline', emergency_contact_relationship = 'Uncle')
    # test_pet3 = Pet(name = 'Yay', profile_pic = 'jpeg', breed = 'lab', age = 1, size = 'big', allergies = True, friendly_w_dogs = False, friendly_w_kids = True, spayed_neutered = True, microchipped = True, pet_owner_id = 2, emergency_phone = 2340987, emergency_contact_name = 'Lana', emergency_contact_relationship = 'mom')

    # test_owner2 = PetOwner(email = 'ownetwo@pets.com', password = 'ownetwo', fname = 'second', lname = 'owner', profile_pic = 'jpeg', num_pets=1, mobile =22200000, street_address = 'Second Street owner', city = 'Seatest', state = 'Washington', zip_code = 98124)

    # test_sitter2 = Sitter(email = 'testtwo@test.com', password = 'Secondtest', fname = 'Lana', lname = 'Greenwood', profile_pic = 'jpeg', summary = "hello, I'm the second test", years_of_experience = 1, mobile = 11000000, street_address = 'Second Street', city = 'Seatest', state = 'Washington', zip_code = 98124, minute_rate = 0.90)
    
    # db.session.add_all([test_sitter1, test_owner1, test_pet1, test_booking1,test_pet2,test_pet3, test_owner2, test_sitter2])
    # db.session.commit()



if __name__ == "__main__":
    from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
# connect_to_db(app, "dog_walker")

