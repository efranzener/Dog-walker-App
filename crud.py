"""CRUD operations."""

from model import db, User, Sitter, PetOwner, Pet, Vet, Booking, connect_to_db
from flask import session, flash, redirect, render_template

######## CREATE #########

def create_user(fname, lname, email, password, profile_pic, dob, mobile, address, zip_code, city='Seattle', state='Washington'):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, profile_pic=profile_pic, dob=dob, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code)
 
    return user


def create_sitter(user_id, summary, rate,  years_of_experience=0):
    """Create and return a new sitter."""

    sitter = Sitter(user_id = user_id, summary = summary, rate=rate, years_of_experience=years_of_experience)

    return sitter


def create_pet_owner(user_id, num_pets):
    """Create and return a new pet_owner."""

    pet_owner = PetOwner(user_id = user_id, num_pets = num_pets)
    
    return pet_owner


def create_pet(name, profile_pic, breed, age, size, allergies, allergies_kind, house_trained, friendly_w_dogs, friendly_w_kids, spayed_neutered, microchipped, additional_info, emergency_phone, emergency_contact_name, emergency_contact_relationship, pet_owner_id):
    """Create and return a new pet"""
 
    pet = Pet(name=name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, house_trained = house_trained, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, additional_info = additional_info, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owner_id = pet_owner_id)

    return pet


def create_vet(fname: str, lname: str, mobile: int, address: str, zip_code: str, pet_id: int, city='Seattle', state='Washington'):
    """ Create and return a new vet"""

    vet = Vet(fname=fname, lname=lname, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, pet_id = pet_id)
    
    return vet


def create_booking(weekly, pet_id, sitter_id, pet_owner_id, start_time, end_time, start_date, end_date):
    """Create and return a new booking"""

    booking = Booking(pet_id=pet_id, pet_owner_id=pet_owner_id, sitter_id=sitter_id, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, weekly=weekly)
    db.session.add(booking)
    db.session.commit()
    return booking


# def create_recurring_booking(weekly, pet_id, sitter_id, pet_owner_id, start_time, end_time, start_date, end_date, interval):
#     """create a recurring booking"""
    
    
    
######## GET #########

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
 
 
def get_petowner_by_id(id):
    """Return a pet_owner by primary key."""

    return PetOwner.query.get(id)


def get_petowner_by_user_id(user_id):
    """Return a pet_owner by user_id."""

    return PetOwner.query.filter(Pet.user_id == user_id).first()


def get_pets_by_ownerid(pet_owner_id):
    """return all pets from a specific pet owner id"""
    
    if Pet.query.filter(Pet.pet_owner_id == pet_owner_id).first() != None:
        total_pets = Pet.query.filter(Pet.pet_owner_id == pet_owner_id).all()
        print(total_pets)
    else:
        print("No pets registered yet")
        total_pets = 0

    return total_pets
 
 
def get_total_pets_by_owner(pet_owner_id):
    """return the total count of pets by a specific owner"""     
        
    return Pet.query.filter(Pet.pet_owner_id == pet_owner_id).count()


def get_user_by_id(user_id):
    """Return a user by primary key."""


    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_bookings_by_pet_owner(pet_owner_id):
    """Return all the bookings from a specific pet owner"""

    if Booking.query.filter(Booking.pet_owner_id == pet_owner_id).first() != None:

        return Booking.query.filter(Booking.pet_owner_id == pet_owner_id).all()
    else:
        flash("Sorry you don't have any bookings yet")

        return False


def get_sitters():
    """Return all sitters."""
    
    return Sitter.query.all()
    
    
def get_sitter_by_user_id(user_id):
    """Return a sitter by user_id"""

    return Sitter.query.filter(Sitter.user_id == user_id).first()


def get_sitter_by_id(id):
    """Return a sitter by primary key."""

    return Sitter.query.get(id)


def get_sitter_by_email(email):
    """Return a sitter by email."""
    
    return Sitter.query.filter(Sitter.email == email).first()


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





if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    print("connected do db")