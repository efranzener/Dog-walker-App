"""CRUD operations."""

from model import db, User, Sitter, PetOwner, Pet, Vet, Booking, connect_to_db


# def create_sitter(fname, lname, email, password, profile_pic, years_of_experience, mobile, address, zip_code, rate, summary="optional", city='Seattle', state='Washington'):
#     """Create and return a new sitter."""

#     sitter = Sitter(fname=fname, lname=lname, email=email, password=password, profile_pic=profile_pic, years_of_experience=years_of_experience, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, summary = summary, rate=rate)

#     return sitter

def create_user(fname, lname, email, password, profile_pic, dob, mobile, address, zip_code, city='Seattle', state='Washington'):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, profile_pic=profile_pic, dob=dob, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code)
    
    return user

def get_user_by_id(user_id):
    """Return a user by primary key."""
   

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_sitter(user_id, summary, rate,  years_of_experience=0):
    """Create and return a new sitter."""

    # user = User.query.get(id)

    sitter = Sitter(user_id = user_id, summary = summary, rate=rate, years_of_experience=years_of_experience)

    return sitter

def get_sitters():
    """Return all sitters."""

    return Sitter.query.all()


def get_sitter_by_id(id):
    """Return a sitter by primary key."""

    return Sitter.query.get(id)


def get_sitter_by_email(email):
    """Return a sitter by email."""
    
    return Sitter.query.filter(Sitter.email == email).first()


def create_pet_owner(user_id, num_pets):
    """Create and return a new pet_owner."""

    pet_owner = PetOwner(user_id = user_id, num_pets = num_pets)
    
    return pet_owner


def get_pet_owner_by_id(id):
    """Return a pet_owner by primary key."""

    return PetOwner.query.get(id)


def get_pet_owner_by_email(email):
    """Return a pet_owner by email."""

    return PetOwner.query.filter(PetOwner.email == email).first()


def create_pet(name, profile_pic, breed, age, size, allergies, allergies_kind, friendly_w_dogs, friendly_w_kids, spayed_neutered, microchipped, emergency_phone, emergency_contact_name, emergency_contact_relationship, pet_owners_id):
    """Create and return a new pet"""
 
    pet = Pet(name=name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, emergency_phone=emergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship, pet_owners_id = pet_owners_id)

    return pet

def get_pet_by_id(id):
    """Return a pet by primary key."""

    return Pet.query.get(id)


def create_vet(fname: str, lname: str, mobile: int, address: str, zip_code: str, pet_id: int, city='Seattle', state='Washington'):
    """ Create and return a new vet"""

    vet = Vet(fname=fname, lname=lname, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code, pet_id = pet_id)
    
    return vet


def create_booking(weekly, pet: Pet, sitter_id, pet_owners_id):
    """Create and return a new booking"""

    booking = Booking(weekly=weekly, pet=pet, pet_owners_id=pet_owners_id, sitter_id=sitter_id)

    return booking



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    print("connected do db")