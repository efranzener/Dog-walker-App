import crud
import datetime as dt
from datetime import datetime, timedelta
import pytz
import os

from flask import request


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

tz = pytz.timezone('US/Pacific')  

# Google Calendar API
def get_consent():
    """get user consent to accessing sensitive data"""
    
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)
    
    return service


def get_available_sitters(alternative_id):
    """ query for available sitters based on Google Calendar"""
    
    service = get_consent() 
   
    start_date = request.form.get("start_date")
    start_time = request.form.get("start_time")
    
    starttime_with_date = start_date + "T" + start_time
    starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

    # create an interval to calculate end time, based on 30 min walks
    interval = dt.timedelta(minutes=30)
    end_time =  starttime_datetime + interval
    
    current_user = crud.get_user_by_alternative_id(alternative_id)
    sitters = crud.get_all_other_sitters(current_user.user_id)
    cal_ids = []
    for sitter in sitters:
        calendar_ids={
            "id":sitter.user.email}
        cal_ids.append(calendar_ids)
       
    tz = pytz.timezone('US/Pacific')    
    start_datetime = tz.localize(starttime_datetime)
    end_datetime = tz.localize(end_time)
    body = {
        "timeMin": start_datetime.isoformat(),
        "timeMax": end_datetime.isoformat(),
        "timeZone": 'US/Pacific',
        "items": cal_ids
    }
    eventsResult = service.freebusy().query(body=body).execute()
    
    cal_dict = eventsResult['calendars']
    available_sitters = []
    for cal_name in cal_dict:
        cal_busy = cal_dict[cal_name]['busy']
    
        if cal_busy != []:
            continue
        else:
            available_sitters.append(cal_name)

    return available_sitters






def create_cal_bokng(start_date, start_time, user_id, sitter_id, pet_id, address, description):
    """insert a new_booking into google calendar"""
    
    service = get_consent()
    
    user = crud.get_user_by_id(user_id)
    sitter = crud.get_user_by_id(sitter_id)
    pet = crud.get_pet_by_id(pet_id)
    sitter_user = crud.get_user_by_id(sitter.user_id)
    pet_name = pet.name
    sitter_name = (sitter_user.fname) +" "+(sitter_user.lname)
    pet_owner_name = (user.fname) +" "+ (user.lname)
    
    # start_date = request.form.get("start_date")
    # start_time = request.form.get("start_time")
    print("im the start time", start_time, "and aim the start date", start_date)
    # starttime_with_date = start_date + "T" + start_time
    
    # starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

    starttime_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

    # create an interval to calculate end time, based on 30 min walks
    interval = dt.timedelta(minutes=30)
    end_time =  starttime_datetime + interval

    print("Im the end_time", end_time, type(end_time))
    tz = pytz.timezone('US/Pacific')    
    start_datetime = tz.localize(start_date)
    end_datetime = tz.localize(end_time)
    body = {
        "summary":f"Dog Walk for {pet.name}" ,
        "description":description,
        "location": address,
        "transparency": "opaque",
        "visibility": "private",
        "start":{
            "dateTime": start_datetime.isoformat(),
            "timeZone": 'US/Pacific',
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": 'US/Pacific',
        },
        
        "attendes": [
            {'email': user.email},
            {'email': sitter_user.email},
            
            {'petname': pet_name},
            {'petOwner': pet_owner_name},
            {'Sitter': sitter_name}
        ],
        "reminders": {
            "useDefault": True
            }
    }
    
    event = service.events().insert(calendarId=sitter_user.email,  body=body).execute()
    
    return event


def free_times(selected_date, sitter_id):
    """ Given a date, and a sitter, returns a list with available times """

    service = get_consent()
    sitter = crud.get_sitter_by_id(sitter_id)
    cal_id={"id":sitter.user.email}
    start_time = selected_date + "T" + "06:00"
    end_time = selected_date + "T" + "06:30"
    max_end_time = selected_date + "T" + "23:30"

    
    starttime_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    endtime_datetime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    
    start_datetime = tz.localize(starttime_datetime)
    end_datetime = tz.localize(endtime_datetime)

    max_end_datetime = datetime.strptime(max_end_time, "%Y-%m-%dT%H:%M")
    max_datetime = tz.localize(max_end_datetime)

    available_times = []
    while start_datetime <= max_datetime:
        
        body = {
            "timeMin": start_datetime.isoformat(),
            "timeMax": end_datetime.isoformat(),
            "timeZone": 'US/Pacific',
            "items": [
                {
                "id": cal_id
                }
            ]
        }
        eventsResult = service.freebusy().query(body=body).execute()
        cal_dict = eventsResult['calendars']
    
        for cal_name in cal_dict:
            cal_busy = cal_dict[cal_name]['busy']
        
            if cal_busy == []:
                start_time = body["timeMin"]
                available_times.append(start_time)
            else: 
                continue
        start_datetime = start_datetime + timedelta(minutes=30)
        end_datetime = end_datetime + timedelta (minutes=30)

    return available_times

def retrive_booking(calendarId, eventId):
    """get a specidif booking from google calendar"""

    service = get_consent()

    event = service.events().get(calendarId=calendarId, eventId=eventId).execute()

    return event
        
 
def update_booking(google_booking_id, calendar_id):
    """update a booking on the google calendar"""

    service = get_consent()


    new_start_date = request.form.get("new_date")
    new_start_time = request.form.get("new_time")
    starttime_with_date = new_start_date + "T" + new_start_time
    
    starttime_datetime = datetime.strptime(starttime_with_date, "%Y-%m-%dT%H:%M")

    # create an interval to calculate end time, based on 30 min walks
    interval = dt.timedelta(minutes=30)
    end_time =  starttime_datetime + interval

    tz = pytz.timezone('US/Pacific')    
    start_datetime = tz.localize(starttime_datetime)
    end_datetime = tz.localize(end_time)
    
    event = retrive_booking(calendar_id, google_booking_id)
    event['start'] ['dateTime']: start_datetime.isoformat()
    event['start']['timeZone']: tz
    event['end']['dateTime']: end_datetime.isoformat()
    event['end']['timeZone']: tz


    updated_event = service.events().update(calendarId=calendar_id, eventId=google_booking_id, body=event).execute()
    print (updated_event['updated'])
    return updated_event
    
# First retrieve the event from the API.


        

       