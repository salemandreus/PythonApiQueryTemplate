# A template for using python to query a restful API using GET, POST and PATCH statements
# Example here creates a user account, generates an api key, then modifies practitioners on a flatform and ads and modifies appointment data from that account.

import requests
import json
import os

# Import Env Variables you've set in a previous script
username = os.environ['API_USERNAME']
email = os.environ['API_ACCOUNT_EMAIL']
password = os.environ['API_PASSWORD']
apiUrl = os.environ['API_BASEURL']
firstname = os.environ['API_ACCOUNT_FIRSTNAME']
lastname = os.environ['API_ACCOUNT_LASTNAME']

# Customise Header
head = {
    "Content-Type": "application/json"
}

# 1 Create Account
# Customise Body
body = {
  "username": username,
  "password": password,
  "email": email,
  "first_name": firstname,
  "last_name": lastname
  
}
response = requests.post(apiUrl +'/user/', headers = head, data=json.dumps(body))

#2. Log in/Get API Key
head = {
    "Content-Type": "application/json"
}

body = {
    "username": username,
    "password": password
}

response = requests.post(apiUrl +'/login/', headers = head, data=json.dumps(body))
jsonResponse = json.loads(response.text)
api_key = jsonResponse["api_key"]

 # Apikey Access
head = {
    "Content-Type": "application/json",
    "authorization": "apikey " + username +":" + api_key
}

#3. Get User Data
response = requests.get(apiUrl +'/user/',  headers = head)
jsonResponse = json.loads(response.text)
userId = str(jsonResponse['objects'][0]["id"])

##4. Update User
body = {
  "first_name": "Joe Soap"
}

response = requests.patch(apiUrl + '/user/' + userId + '/', headers = head, data=json.dumps(body))

#5. Create Workplace
body = {
  "name": "Dr X's Office",
  "latitude": -33.93163,
  "longitude": 18.46562
}

response = requests.post(apiUrl + '/workplace/', headers = head, data=json.dumps(body))


#6. Create Practitioner
body = {
  "title": "Dr.",
  "first_name": "First Name",
  "last_name": "Last Name",
  "contact_email": "If different from User.email",
  "contact_number": "01234567890",
  "registration_number": "HPCSA number",
  "caption": "Professional Statement",
  "workplaces": [ "/api/v1/workplace/1/" ],
  "professions": [ "/api/v1/profession/1/", "/api/v1/profession/2/" ],
  "languages": [ "/api/v1/language/1/", "/api/v1/language/2/" ]
}

response = requests.post(apiUrl + '/practitioner/', headers = head, data=json.dumps(body))


#7 Add Contact Details
jsonResponse = json.loads(response.text)
practitioner_id = str(jsonResponse["practitioner_id"])
workplace_id = str(jsonResponse['workplaces'][0]["workplace_id"])

body = {
    "objects": [
      {
         "practitioner": "api/v1/practitioner/" + practitioner_id + "/",
         "workplace": "api/v1/workplace/" + workplace_id + "/",
         "contact_detail": {
            "contact_detail_type": "/api/v1/contact_detail_type/1/",
            "label": "Primary phone number",
            "value": "0123456789"
         }
      },
      {
         "practitioner": "api/v1/practitioner/" + practitioner_id + "/",
         "workplace": "api/v1/workplace/" + workplace_id + "/",
         "contact_detail": {
            "contact_detail_type": "/api/v1/contact_detail_type/3/",
            "label": "Primary email address",
            "value": "someone@example.com"
         }
      },
      {
         "practitioner": "api/v1/practitioner/" + practitioner_id + "/",
         "workplace": "api/v1/workplace/" + workplace_id + "/",
         "contact_detail": {
            "contact_detail_type": "/api/v1/contact_detail_type/3/",
            "label": "Secondary email address",
            "value": "someone2@example.com"
         }
      }
    ]
  }
  
response = requests.patch(apiUrl + '/practitioner_contactdetail/', headers = head, data=json.dumps(body))

# 7.6 Get list of contact detail types
response = requests.get(apiUrl + '/contact_detail_type/', headers = head)

# 8 Configure Opening Times
body = {
  "objects": [
    {
        "workplace": "/api/v1/workplace/" + workplace_id +"/",
        "practitioner": "/api/v1/practitioner/" + practitioner_id + "/",
        "day_of_week": 0,
        "start_time": "09:00",
        "end_time": "13:00",
        "timeslot_length": 30
    },
    {
        "workplace": "/api/v1/workplace/" + workplace_id + "/",
        "practitioner": "/api/v1/practitioner/" + practitioner_id + "/",
        "day_of_week": 0,
        "start_time": "14:00",
        "end_time": "17:00",
        "timeslot_length": 30
    },
    {
        "workplace": "/api/v1/workplace/" + workplace_id + "/",
        "practitioner": "/api/v1/practitioner/" + practitioner_id + "/",
        "day_of_week": 1,
        "start_time": "09:00",
        "end_time": "17:00",
        "timeslot_length": 30
    }
  ]
}

response = requests.patch(apiUrl + '/opening_time/', headers = head, data=json.dumps(body))

# 9 Get available time slots
response = requests.get(apiUrl + '/dynamic_time_slot/' + practitioner_id + "/" + workplace_id + '/2019-03-22T10h00/2019-03-27T11h00/true', headers = head, data=json.dumps(body))

# 10 Book appointment
body = {
    "practitioner": "/api/v1/practitioner/9934/",
    "workplace": "/api/v1/workplace/" + workplace_id + "/",
    "patient_name": "Joe Everyman",
    "contact_number": "072 897 6543",
    "email": "joe.everyman@gmail.com",
    "confirmation_state": "pending",
    "existing_patient": False,
    "reason_for_visit": "General Check-up",
    "date": "2014-12-12",
    "time": "14:30",
    "duration": 30
}

response = requests.post(apiUrl + '/appointment/', headers = head, data=json.dumps(body))

# 11 - Confirm Appointment 
jsonResponse = json.loads(response.text)
appointment_id = str(jsonResponse["appointment_id"])

body = {
  "confirmation_state": "confirmed"
}

response = requests.patch(apiUrl + '/appointment/' + appointment_id + '/', headers = head, data=json.dumps(body))
