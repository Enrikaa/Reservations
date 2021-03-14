1. Paziurek video apie REST API 
2. Paziurek vidoe apie Django Rest Framework (DRF)
3. susikurt modelius
4. api endpoint
    1. Get meeting room reservation
        - URL: 'room/<room_id>'
        - Reservation - issfiltruot rezervacijas su room_id
        - status - `Scheduled`, o ne `Canceled` / `Ended` - filtruoti tik Scheduled
        - 
    2. Create reservation 
        - Post request 
        - Turi nurodyt Room id
        - Employees ids

    3. Cancel reservation
        - PUT request
        - url: 'reservation/<reservation_id>/cancel
        - 

1. How to get Room Reservations
 - send GET request to `/room/<room_id>`
    - room_id - id of room
