"""Models for dog walker app"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timedelta
import os

from enum import Enum

app = Flask(__name__)
db = SQLAlchemy()



class User(db.Model):
    """ A user"""
    
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    dob = db.Column(db.Date, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable = False)
    profile_pic = db.Column(db.String(300), nullable=False, default='https://res.cloudinary.com/dggbnnudv/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1663617415/profile_standard_wtcydo.jpg')
    mobile = db.Column(db.String(15), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(50), default = "Seattle",nullable = False)
    state = db.Column(db.String(20),default = "Washington", nullable = False)
    zip_code = db.Column(db.String(5), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # pet_owner = a PetOwner object
    # sitter = a Sitter object

def __repr__(self):
    """Show info about user"""

    return f'<User user_id={self.user_id}, fname={self.fname}, lname={self.lname}, dob={self.dob}, email={self.email}, password={self.password}, profile_pic={self.profile_pic}, mobile={self.mobile}, address={self.address}, city={self.city}, state={self.state}, zip_code={self.zip_code}>'



class Sitter(db.Model):
    """ A pet sitter"""

    __tablename__ = 'sitters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique = True, nullable = False)
    summary = db.Column (db.Text, default =  "Optional")
    years_of_experience = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


    user = db.relationship("User", uselist=False, backref="sitter")
    # bookings = a list of Booking objects


def __repr__(self):
    """Show info about sitter"""

    return f'<Sitter summary={self.summary}, experience={self.years_of_experience}, rate={self.rate}>'



class PetOwner(db.Model):
    """A pet's owner"""

    __tablename__ = "pet_owners"   

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique = True, nullable = False)
    num_pets = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    # bookings = a list of Booking objects
    

    pets = db.relationship('Pet', backref = "pet_owner")
    user = db.relationship("User", uselist=False, backref="pet_owner")


def __repr__(self):
    """Show info about pet owner"""

    return f"<PetOwner  num_pets = {self.num_pets}>"
    



class Pet(db.Model):
    """A pet"""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    profile_pic = db.Column(db.String(300))
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
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # bookings = a list of Booking objects
    # vet = a Vet object



def __repr__(self):
    """Show info about pet"""

    return f"<Pet id={self.pet_id}, name = {self.name}, profile_pic = {self.profile_pic}, breed = {self.breed}, age = {self.age}, size = {self.age}, allergies = {self.allergies}, house_trained = {self.house_trainded}, friendly_w_dogs = {self.friendly_w_dogs}, friendly_w_kids = {self.friendly_w_kids}, spayed_neutured = {self.spayed_neutered}, microchipped = {self.microchipped}, emergency_phone = {self.emergency_phone}, emergency_contact_name = {self.emergency_contact_name}, emergency_contact_relationship = {self.emergency_contact_relationship} pet>"

    
class Status(Enum):
    """Class to handle status options """
    
    Pending = 'Pending'
    Confirmed = 'Confirmed'
    Declined = 'Declined'
    Cancelled = 'Cancelled'
    
    

class Booking(db.Model):
    """A booking info"""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    status = db.Column(db.Enum(Status), default="Pending", nullable = False)
    pet_owner_id = db.Column(db.Integer, db.ForeignKey("pet_owners.id"))
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.id"))
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    start_date = db.Column(db.DateTime, default=datetime.now().strftime("%x"), nullable = False)
    end_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(days=180)).strftime("%x"), nullable = False)
    start_time = db.Column(db.DateTime, default=datetime.now().strftime("%H:%M"), nullable = False)
    end_time = db.Column(db.DateTime, default=(datetime.now() + timedelta(minutes=30)).strftime("%H:%M"), nullable = False)
    weekly = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    pet = db.relationship("Pet", backref = 'bookings',)
    sitter = db.relationship("Sitter", backref = 'bookings', )
    pet_owner = db.relationship("PetOwner", backref = 'bookings', )


def __repr__(self):
    """Show info about booking"""

    return f"<Booking id={self.id}, start_date={self.start_date}, end_date={self.end_date}, start_time={self.start_time}, end_time={self.end_time}>"


def connect_to_db(flask_app, db_uri="postgresql:///dog_walkers", echo=True):
    """Connect to database."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    

if __name__ == "__main__":
    from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

 
    connect_to_db(app)

   


