"""CRUD operations."""

from model import db, User, Sitter, PetOwner, Pet, Booking, connect_to_db
from flask import session, flash, redirect, render_template


######## CREATE #########

def create_user(fname, lname, email, password, profile_pic, dob, mobile, address, zip_code, city='Seattle', state='Washington', authenticated=False,):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, authenticated=authenticated, profile_pic=profile_pic, dob=dob, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code)
    db.session.add(user)
    db.session.commit()

    return user


def create_sitter(user_id, summary, rate,  years_of_experience):
    """Create and return a new sitter."""

    sitter = Sitter(user_id = user_id, summary = summary, rate=rate, years_of_experience=years_of_experience)
    db.session.add(sitter)
    db.session.commit()
        
    return sitter


def create_pet_owner(user_id, num_pets):
    """Create and return a new pet_owner."""

    pet_owner = PetOwner(user_id = user_id, num_pets = num_pets)
    db.session.add(pet_owner)
    db.session.commit()
    
    return pet_owner


def create_pet(name, profile_pic, breed, age, size, allergies, allergies_kind, house_trained, friendly_w_dogs, friendly_w_kids, spayed_neutered, microchipped, additional_info, emergency_phone, emergency_contact_name, emergency_contact_relationship, pet_owner_id):
    """Create and return a new pet"""
 
    pet = Pet(name=name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, house_trained = house_trained, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, additional_info = additional_info, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owner_id = pet_owner_id)
    db.session.add(pet)
    db.session.commit()     
    return pet


def create_booking(weekly, pet_id, sitter_id, pet_owner_id, start_time, end_time, start_date, end_date):
    """Create and return a new booking"""

    booking = Booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, weekly=weekly)
   
    db.session.add(booking)
    db.session.commit() 
     
    return booking

    
    
# CHECK IF REGISTERED
    

    
def sitter_exists(user_id):
    """ return whether sitter exists or not """

    if Sitter.query.filter(Sitter.user_id == user_id).first() != None:
        
        return True
    else:
        return False


def petowner_exists(user_id):
    """ return whether pet_owner exists or not """
    
    if PetOwner.query.filter(PetOwner.user_id == user_id).first() != None:
        return True
    else:
        return False
 

def pet_exists(pet_owner_id, name):
    """ Return True if pet already exists in DB"""

    if Pet.query.filter(Pet.name == name, Pet.pet_owner_id == pet_owner_id).first() != None:
        return True
    else:
        return False
    
    ######## GET #########

    
def get_all_other_users(user_id):
    """Return all users excepts the current user id"""

    return User.query.filter(user_id != user_id).all()


    
def get_sitter_by_user_id(user_id):
    """Return a sitter by user id"""

    return Sitter.query.filter(Sitter.user_id == user_id).first()


def get_petowner_by_user_id(user_id):
    """Return a pet_owner by user_id."""

    return PetOwner.query.filter(Pet.user_id == user_id).first()


def get_pets_by_ownerid(pet_owner_id):
    """return all pets from a specific pet owner id"""
    
    if Pet.query.filter(Pet.pet_owner_id == pet_owner_id).first() != None:
        total_pets = Pet.query.filter(Pet.pet_owner_id == pet_owner_id).all()
    else:
        total_pets = 0

    return total_pets
 
 
def get_total_pets_by_owner(pet_owner_id):
    """return the total count of pets by a specific owner"""     
        
    return Pet.query.filter(Pet.pet_owner_id == pet_owner_id).count()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_sitter_id(sitter_id):
    """Returns a user assiciated with a certain sitter id"""
        
    sitter = get_sitter_by_id(sitter_id)
    user_id = sitter.user_id
    user = get_user_by_id(user_id)

    return user


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_sitter_bookings_by_user_id(user_id):
    """Return all the sitter bookings from a specific user_id"""

    sitter = get_sitter_by_user_id(user_id)
    s_bookings = []
    if (Booking.query.filter(Booking.sitter_id == sitter.id).first()) != None:

        s_bookings = (Booking.query.filter(Booking.sitter_id == sitter.id).all())

    return s_bookings


def get_owner_bookings_by_user_id(user_id):
    """Return all the pet_owner bookings from a specific user_id"""

    pet_owner = get_petowner_by_user_id(user_id)
    owner_bookings = []
    if (Booking.query.filter(Booking.pet_owner_id == pet_owner.id).first()) != None:

        owner_bookings = Booking.query.filter(Booking.pet_owner_id == pet_owner.id).all()

    return owner_bookings

def get_booking_by_id(booking_id):
    "return a booking with the specified id"
    
    return Booking.query.get(booking_id)


def get_sitters():
    """Return all sitters."""
    
    return Sitter.query.all()  


def get_sitter_by_id(sitter_id):
    """Return a sitter by primary key."""

    return Sitter.query.get(sitter_id)


def get_sitter_by_user_id(user_id):
    """Return a sitter by user_id."""
    
    return Sitter.query.filter(Sitter.user_id == user_id).first()


def get_all_other_sitters(user_id):
    """Return all sitters excepts the current user_id"""
    
    return Sitter.query.filter(Sitter.user_id != user_id).all()


def get_petowner_by_user_id(user_id):
    """Return a pet_owner by user_id"""
    
    return PetOwner.query.filter(PetOwner.user_id == user_id).first()


def get_pet_by_id(id):
    """Return a pet by primary key."""

    return Pet.query.get(id)


def delete_user(user_id):
    
    user = get_user_by_id(user_id)
    db.session.delete(user)
    db.session.commit()

    return None



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
