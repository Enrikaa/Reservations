# OVERVIEW

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

> Everything can be checked in POSTMAN and Django Rest Framework. Below are instructions to help test the API in a POSTMAN.First needed to create super user and make login. From login will receive "auth_token". Having this key gives access to everyone API endpoint.

### CREATE SUPER USER

* Create super user (three options: TerminaL, POSTMAN, Django rest framework):
   - Terminal:
       ```sh
     python manage.py createsuperuser
       ```
   - POSTMAN:
       ```sh
      http://127.0.0.1:8000/api/v1/users/
        ```
      Write your super user data in POSTMAN -> Body -> formatdata/raw/json

### GET AUTH TOKEN

* Get token from authentication:
   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/token/login/
       ```
     - Make POST request and take auth_token from login

### CHECK AUTHENTICATION SUCCESSFULY

3. Verify that the authentication was successful:
   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/authentication/checker/
       ```
     - Make GET request and use "auth_token" from login in this endpoint. "Headers -> KEY: Authorization -> VALUE: Token {{token}}". If authentication is successful, you should see "Information just for logged in Users", if not - "Authentication credentials were not provided"
     - Also need to write super user data in " Body -> formatdata/raw/json". Required fields are: "Email", "Username", "First Name", "Last Name", "Password"

### CHECK ALL EXISTING ROOMS, RESERVATIONS AND RESERVATIONS BY ID

4. Check all existing rooms:

   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/rooms/all/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make GET request and check all existing rooms

5. Check all existing reservations:

   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/reservations/all/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make GET request and check all existing reservations

6. Check reservation by id:
   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/reservation/26/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make GET request and check reservation details by reservation id

### GET MEETING ROOM RESERVATIONS, CREATE RESERVATION, CANCEL RESERVATION

7. Get meeting room reservations:

   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/reservations/room/2/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make GET request and check meeting room reservations

8. Create reservation:

   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/create/reservation/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make POST request and create reservation

9. Cancel reservation

   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/reservation/delete/27/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make DELETE request and delete reservation by id

### LOGOUT

10. Cancel reservation

   - In POSTMAN USE THIS ENDPOINT:
       ```sh
     - http://127.0.0.1:8000/api/v1/token/logout/
       ```
     - Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
     - Make POST request and logout




# Docker

- run: `docker-compose up --build`.
