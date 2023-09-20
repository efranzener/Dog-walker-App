# VowVow Dog Walkers

A full stack web application for dog owners to find and book dog walkers.

## Overview ##
---
Walk though video coming soon.

* Users can create an account and then login to finish their pet-owner and/or sitter profile, which uses Cloudinary API for picture storage.

* After creating their dog(s) profile, a pet-owner can search for a sitter using date and time filters.

* Google calendar is used to query for available sitters, and once a pet owner creates a new booking, this is then added to the sitter's calendar. 

* Bookings for the next 7 days are displayed in the user's dashboard, while the remaining and past ones are displayed in all-bookings tab.


### Motivation ###
---

My motivation to build this web application came from my experience using several pet-sitter apps during my time working as a dog walker.


### Technologies ###
---

This project was created with:

* Backend: Python 3.7, Flask, SQLAlchemy, PostgreSQL 

* Frontend: Java Script, HTML, CSS, Bootstrap, Jinja2, AJAX

* Libraries: Flask Bcrypt, Flask-Login



### <a name="api"></a> API'S ###

* [Cloudinary API](https://cloudinary.com/documentation/python_quickstart)

* [Google Calendar API](https://developers.google.com/workspace/guides/get-started)

### SET UP ###
---
#### Prerequisites ####
To run Vowvow Dog Walkers, you must have installed:
 * [PostgreSQL](https://www.postgresql.org/)
 * [Python 3.7](https://www.python.org/downloads/)
 * [API Key for Cloudinary's API](https://cloudinary.com/documentation/python_quickstart)
 * [Google Credentials for Google Calendar API](https://developers.google.com/workspace/guides/get-started)

Clone or fork repository:

``` bash
git clone https://github.com/efranzener/Dog-walker-App
```
Create and activate a virtual environment within your directory

```bash
    virtualenv env source env/bin/activate
```
Install requirements

```bash
pip3 install -r requirements.txt
```

Get a Cloudinary API Key and save it in a file called secrets.sh using this format.

```bash
export cloud_name = "THE_CLOUD_NAME_GOES_HERE"
export cloudinary_api_key=="YOUR API_KEY_GOES_HERE"
export api_secret="YOUR_API_SECRET_GOES_HERE"
```

Sign up to the Google Cloud console to create a OAuth 2.0 Client IDs credential for Desktop app, and define the following scopes of data access for your credentials: 

* https://www.googleapis.com/auth/calendar
* https://www.googleapis.com/auth/calendar.events

Download and save the credentials in a file called credentials.json

Source your keys into your virtual environment:

```bash
source secrets.sh
```

Run model.py to create all SQL database models
Run the app:
```
bash
python3 model.py
```
To run the app from the command line:
```bash 
python3 server.py
```

### About the Developer ###
Etyene Franzener is a Software Engineer based in Seattle, WA. Vowvow Dog Walkers was her first full-stack web application, and it was built as a capstone project for [Hackbright Academy](https://hackbrightacademy.com/), a 6 months full-stack software engineering program.
With a focus on the customer experience, Etyene is eager to learn more and build meaningful products that make people's lives easier. 
