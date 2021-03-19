# Overview

This is a internal services which can get meeting room reservations, create reservation, cancel reservation.

_Created by:_**Enrika Vyšniauskaitė**

#Requirements

- Python => 3.8

# Setup

1. Create and activate a virtual environment (python version => 3.8)
   virtualenv env -p python
   source env/bin/activate
2. Install pip libraries
   pip install -r requirements.pip

#How to run

To try reqruirements for implementation first needed to create SuperUser and make login from which will receive "auth_token". Having this key gives access to everyone API endpoint.

1. Create SuperUser:

   - http://127.0.0.1:8000/api/v1/users/
   - python manage.py createsuperuser ("Email", "Username", "First Name", "Last Name", "Password")
   - or create SuperUser in Django REST framework.

2. Login:

   - http://127.0.0.1:8000/api/v1/token/login/
   - Take auth_token from login

3. Verify that the authentication was successful:

   - http://127.0.0.1:8000/api/v1/authentication/checker/
   - Put "auth_token" in POSTMAN -> Headers. In KEY field should be: "Authorization" and in KEY field: "Token {{auth_token}}". If successful, you should see "Information just for logged in Users", if not - "Authentication credentials were not provided".

#Additional steps to create reservations:

4. Check all existing rooms:

   - http://127.0.0.1:8000/api/v1/rooms/all/
   - Put "auth_token"in the POSTMAN -> Headers.
   - Or check all existing rooms in Django REST framework.

5. Check all existing reservations:

   - http://127.0.0.1:8000/api/v1/reservations/all/
   - Put "auth_token"in the POSTMAN -> Headers.
   - Or check all existing reservations in Django REST framework.

6. Check reservation by id:

   - http://127.0.0.1:8000/api/v1/reservation/14/
   - Put "auth_token"in the POSTMAN -> Headers.
   - Or check reservation by id in Django REST framework.

#"Reservation" tasks implementation:

7. Get meeting room reservations (check reservations by room id):

   - http://127.0.0.1:8000/api/v1/reservations/room/2/
   - Put "auth_token"in the POSTMAN -> Headers.
   - Or get room reservations in Django REST framework.

8. Create reservation:

   - http://127.0.0.1:8000/api/v1/create/reservation/
   - Put "auth_token"in the POSTMAN -> Headers.
   - Or create reservation in Django REST framework.

9. Cancel reservation
   - In API endpoint you need to write reservetion and reservation id which you want to delete
   - http://127.0.0.1:8000/api/v1/reservation/delete/27/

# Docker

- run: `docker-compose up --build`.
