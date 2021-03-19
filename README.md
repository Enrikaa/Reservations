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

Run the project with Docker
 ```sh
docker-compose up --build
```

> Everything can be checked in Postman and Django Rest Framework. Below are instructions to help test the API in a Postman. First you need to Login to get Auth Token with default user: `admin@admin.com` and password: `admin`. From login you will receive "auth_token". This token gives access to every API endpoint.

In your Postman import API endpoint collection fixture file named: `Reservations.postman_collection.json`

### GET AUTH TOKEN

1. Get token from authentication:
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/token/login/
       ```
        Make POST request and take auth_token from login. Use default credentials username: `admin@admin.com` password: `admin`
        
### CHECK ALL EXISTING ROOMS
2. Check all existing rooms:
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/rooms/all/
       ```
      Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
      Make GET request and check all existing rooms

### CHECK ALL EXISTING RESERVATIONS
3. Check all existing reservations:
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/reservations/all/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make GET request and check all existing reservations

### GET MEETING ROOM RESERVATIONS
4. Get meeting room reservations:
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/reservations/room/1/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make GET request and check meeting room reservations
       
### CREATE RESERVATION
5. Create reservation:
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/create/reservation/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make POST request and create reservation
    - Body example in Postman collection

### CANCEL RESERVATION
6. Cancel reservation
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/reservation/delete/1/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{ token }}"
       Make DELETE request and delete reservation by id

### LOGOUT
7. Logout and destroy token
   - In Postman use this endpoint:
       ```sh
      http://localhost:8000/api/v1/token/logout/
       ```
       Use "auth_token"in the "Headers -> KEY: Authorization -> VALUE: Token {{token}}"
       Make POST request and logout


## Contact
Created by [@enrika](https://www.linkedin.com/in/enrika-vysniauskaite-10bba4196/) - feel free to contact me!

