## Overview

> This is a internal services which can get meeting room reservations, create reservation, cancel reservation.

### TECHNOLOGIES
   * Python
   * Django
   * Django REST framework
   * Djoser
   * Postman
   * PostgreSQL

### SETUP

1. Create and activate a virtual environment (python version => 3.8)
   pip install virtualenv

2. Install requirements.txt
   pip install -r requirements.txt

> Everything can be checked in Postman and Django Rest Framework. Below are instructions to help test the API in a Postman. First needed to create super user and make login. From login will receive "auth_token". Having this key gives access to everyone API endpoint.

### CREATE SUPER USER

1. Create super user (three options: TerminaL, POSTMAN, Django rest framework):
   -  Terminal:
      ```sh
      python manage.py createsuperuser
      ```
   -  Postman:
       ```sh
      http://127.0.0.1:8000/api/v1/users/
        ```
        Write your super user data in Postman -> Body -> formatdata/raw/json


### GET AUTH TOKEN

2. Get token from authentication:
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/token/login/
       ```
        Make POST request and take auth_token from login. Write your super user  email and password in POSTMAN -> Body -> formatdata/raw/json
        
### CHECK ALL EXISTING ROOMS
3. Check all existing rooms:
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/rooms/all/
       ```
      Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
      Make GET request and check all existing rooms

### CHECK ALL EXISTING RESERVATIONS
4. Check all existing reservations:
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/reservations/all/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make GET request and check all existing reservations

### GET MEETING ROOM RESERVATIONS
5. Get meeting room reservations:
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/reservations/room/2/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make GET request and check meeting room reservations
       
### CREATE RESERVATION
6. Create reservation:
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/create/reservation/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make POST request and create reservation

### CANCEL RESERVATION
7. Cancel reservation
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/reservation/delete/27/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make DELETE request and delete reservation by id

### LOGOUT
8. Logout and destroy token
   - In Postman use this endpoint:
       ```sh
      http://127.0.0.1:8000/api/v1/token/logout/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
       Make POST request and logout




# Docker

- run: `docker-compose up --build`.



## Contact
Created by [@enrika](https://www.linkedin.com/in/enrika-vysniauskaite-10bba4196/) - feel free to contact me!

