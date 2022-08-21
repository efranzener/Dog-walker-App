"""Models for dog walker app"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timedelta
import os


app = Flask(__name__)
db = SQLAlchemy()



# *******************
class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    dob = db.Column(db.Date, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable = False)
    profile_pic = db.Column(db.String(300))
    mobile = db.Column(db.String(15), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(50), default = "Seattle",nullable = False)
    state = db.Column(db.String(20),default = "Washington", nullable = False)
    zip_code = db.Column(db.String(5), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


def __repr__(self):
    """Show info about sitter"""

    return f'<User user_id = {self.user_id}, fname = {self.first_name}, lname = {self.last_name}, dob = {self.dob}, email={self.email}, password={self.password}, profile_pic = {self.profile_pic}, mobile = {self.mobile}, address = {self.address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}>'

# ***********************

class Sitter(db.Model):
    """ A pet sitter"""

    __tablename__ = 'sitters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique = True, nullable = False)
    # id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    # email = db.Column(db.String(100), unique=True, nullable=False)
    # password = db.Column(db.String(100), nullable = False)
    # fname = db.Column(db.String(100), nullable = False)
    # lname = db.Column(db.String(100), nullable = False)
    # profile_pic = db.Column(db.String(300))
    summary = db.Column (db.Text, default =  "Optional")
    years_of_experience = db.Column(db.Integer, nullable=False)
    # address = db.Column(db.String(100), nullable = False)
    # city = db.Column(db.String(50), default = "Seattle",nullable = False)
    # state = db.Column(db.String(20),default = "Washington", nullable = False)
    # zip_code = db.Column(db.String(5), nullable = False)
    rate = db.Column(db.Float, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


    user = db.relationship("User", uselist=False, backref="sitter")
    # bookings = a list of Booking objects


# def __repr__(self):
#     """Show info about sitter"""

#     return f'<Sitter id = {self.id}, email={self.email}, password={self.password}, fname = {self.first_name}, lname = {self.last_name}, profile_pic = {self.profile_pic}, summary = {self.summary}, experience = {self.years_of_experience}, mobile = {self.mobile}, address = {self.address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}, minute_rate = {self.minute_rate}>'

def __repr__(self):
    """Show info about sitter"""

    return f'<Sitter  profile_pic = {self.profile_pic}, summary = {self.summary}, experience = {self.years_of_experience}, mobile = {self.mobile}, address = {self.address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}, minute_rate = {self.minute_rate}>'

class PetOwner(db.Model):
    """A pet's owner info"""

    __tablename__ = "pet_owners"   

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique = True, nullable = False)
    # id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    # email = db.Column(db.String(100), unique=True, nullable=False)
    # password = db.Column(db.String(100), nullable = False)
    # fname = db.Column(db.String(100), nullable = False)
    # lname = db.Column(db.String(100), nullable = False)
    # profile_pic = db.Column(db.String(300))
    num_pets = db.Column(db.Integer)
    # mobile = db.Column(db.String(15), nullable = False)
    # address = db.Column(db.String(100), nullable = False)
    # city = db.Column(db.String(50), default = "Seattle", nullable = False)
    # state = db.Column(db.String(20), default = "Washington", nullable = False)
    # zip_code = db.Column(db.String(5), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # bookings = a list of Booking objects
    
    pets = db.relationship('Pet', backref = "pet_owners")
    user = db.relationship("User", uselist=False, backref="pet_owners")


def __repr__(self):
    """Show info about pet owner"""

    return f"<PetOwner  num_pets = {self.num_pets}>"
    
#  def __repr__(self):
#     """Show info about pet owner"""

#     return f'<PetOwner id = {self.id}, email={self.email}, password={self.password}, fname = {self.first_name}, lname = {self.last_name}, profile_pic = {self.profile_pic}, mobile = {self.mobile}, address = {self.address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}, num_pets = {self.num_pets}>'

    


class Pet(db.Model):
    """A pet info"""

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

    return f"<Pet id ={self.id}, name = {self.name}, profile_pic = {self.profile_pic}, breed = {self.breed}, age = {self.age}, size = {self.age}, allergies = {self.allergies}, friendly_w_dogs = {self.friendly_w_dogs}, friendly_w_kids = {self.friendly_w_kids}, spayed_neutured = {self.spayed_neutered}, microchipped = {self.microchipped}, emergency_phone = {self.emergency_phone}, emergency_contact_name = {self.emergency_contact_name}, emergency_contact_relationship = {self.emergency_contact_relationship}>"


class Vet(db.Model):
    """A pet's vet info"""

    __tablename__ = "vets"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    mobile = db.Column(db.String(15), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    city = db.Column(db.String(50), default = "Seattle", nullable = False)
    state = db.Column(db.String(20), default = "Washington",nullable = False)
    zip_code = db.Column(db.String(5), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    pets = db.relationship("Pet", backref = 'vet')


def __repr__(self):
    """Show info about Vet"""

    return f"<Vet id ={self.id}, first_name = {self.first_name}, last_name = {self.last_name}, mobile = {self.mobile}, address = {self.address}, city = {self.city}, state = {self.state}, zip_code = {self.zip_code}>"
    

class Booking(db.Model):
    """A booking info"""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pet_owner_id = db.Column(db.Integer, db.ForeignKey("pet_owners.id"))
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.id"))
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    start_date = db.Column(db.DateTime, default=datetime.now().strftime("%x"), nullable = False)
    end_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(days=180)).strftime("%x"), nullable = False)
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable = False)
    end_time = db.Column(db.DateTime, default=datetime.now() + timedelta(hours=24), nullable = False)
    weekly = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    pet = db.relationship("Pet", backref = 'bookings')
    sitter = db.relationship("Sitter", backref = 'bookings')
    pet_owner = db.relationship("PetOwner", backref = 'bookings')


def __repr__(self):
    """Show info about booking"""

    return f"<Booking id ={self.id}, start_date = {self.start_date}, end_date = {self.end_date}, start_time = {self.start_time}, end_time = {self.end_time}>"


def connect_to_db(app, db_uri="postgresql:///dog_walkers", echo=True):
    """Connect to database."""

#   this is the code that runs with seed.py 
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    # app.config["SQLALCHEMY_ECHO"] = False
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # db.app = app
    # db.init_app(app)
    
    
    # this is the test code without seeding the database, trying to add users through the sign up form
    # os.system("dropdb dog_walkers --if-exists")
    # os.system("createdb dog_walkers")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    


if __name__ == "__main__":
    from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
   


