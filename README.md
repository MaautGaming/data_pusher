# data_pusher

An backend system to trigger sending data to different api.

## Steps to run:

[]clone this repo:

[] Change directory `cd data_pusher`.

[] Run file: `python manage.py runserver 0.0.0.0:8000`

## Avaliable API:

`/account/`  Allowd method = ['GET', 'POST']
`/account/<int:pk>` Allowd method = ['GET', 'PUT', "DELETE"]
`/destination/`      Allowd method = ['GET', 'POST']
`/destination/?account_id=<uuid>`    Allowd method = ['GET', 'POST']
`/destination/<int:pk>`   Allowd method = ['GET', 'PUT', "DELETE"]
`/server/incoming_data/`   Allowd method = ['POST']

### Create a URL to get destinations available for the account when the account id is given as input.

This point 3 of process mentioned above is cover in the list destination api.