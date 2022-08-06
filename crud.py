"""CRUD operations."""

from model import db, Sitter, PetOwner, Pet, Vet, Booking, connect_to_db



def create_sitter(email, password, fname, lname, profile_pic,summary, years_of_experience, mobile, street_address, city, state, zip_code, minute_rate):
    """Create and return a new sitter."""

    sitter = Sitter(email=email, password=password, fname=fname, lname=lname, profile_pic=profile_pic, summary=summary, years_of_experience= years_of_experience, mobile=mobile, street_address=street_address, city=city, state=state, zip_code=zip_code,minute_rate=minute_rate)

    return sitter


def create_pet_owner(email, password, fname, lname, profile_pic, num_pets, pets, mobile, street_address, city, state, zip_code):
    """Create and return a new pet_owner."""

    pet_owner = PetOwner(email=email, password=password, fname=fname, lname=lname, profile_pic=profile_pic, num_pets=num_pets, pets=pets, mobile=mobile, street_address=street_address, city=city, state=state, zip_code=zip_code)

    return pet_owner


def create_pet(name, profile_pic, breed, age, size, allergies, allergies_kind, friendly_w_dogs, friendly_w_kids, spayed_neutered, microchipped, emmergency_phone, emergency_contact_name, emergency_contact_relationship):
    """Create and return a new pet"""
 
    pet = Pet(name=name, profile_pic=profile_pic, breed=breed, age=age, size=size, allergies=allergies, allergies_kind=allergies_kind, friendly_w_dogs=friendly_w_dogs, friendly_w_kids=friendly_w_kids, spayed_neutered=spayed_neutered, microchipped=microchipped, emmergency_phone=emmergency_phone, emergency_contact_name=emergency_contact_name, emergency_contact_relationship=emergency_contact_relationship)

    return pet


def create_vet(pet, fname, lname, mobile, address, city, state, zip_code):
    """ Create and return a new vet"""

    vet = Vet(pet=pet, fname=fname, lname=lname, mobile=mobile, address=address, city=city, state=state, zip_code=zip_code)
    
    return vet

def create_booking(start_date, end_date, start_time, end_time, weekly, pet, sitter, pet_owner):
    """Create and return a new booking"""

    booking = Booking(start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, weekly=weekly, pet=pet, pet_owner=pet_owner, sitter=sitter)

    return booking



if __name__ == '__main__':
    from server import app
    connect_to_db(app)