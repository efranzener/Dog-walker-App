# #print("hello")
# import json

# class SignupRequest(dict):
#     def __init__(self, name: str, email: str, age: int):
#         self.name = name
#         self.email = email
#         self.age = age

# newSignup = SignupRequest("Ety", "ety@gmail.com", 12)

# print("name: ", newSignup.name)
# newSignupJson = json.dumps(newSignup.__dict__)
# print("newSignupJson: ", newSignupJson)

import google.oauth2.credentials
import google_auth_oauthlib.flow

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/calendar.events.freebusy'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = "http://localhost:5000"

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    prompt='consent',
    include_granted_scopes='true')
