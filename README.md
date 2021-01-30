# Lenme_test
# Requirements

* Python (3.5, 3.6, 3.7, 3.8, 3.9)
* Django (2.2, 3.0, 3.1)

it's **highly recommend** and only officially support the latest patch release of
each Python and Django series.

# Installation DRF

Install using `pip`...

    pip install djangorestframework

Add `'rest_framework'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = [
        ...
        'rest_framework',
    ]

# Creating Migrations


	* python manage.py makemigrations lenme
   
	* python manage.py migrate
   
# Run Server


	* python manage.py runserver

# create superuser


	* python manage.py createsuperuser

# Testing
To run the tests, run


	* python manage.py test


# Endpoints
```

GET  /lenme/list-investors

GET  /lenme/list-investors/<int:pk>

GET  /lenme/list-investors/<int:pk>/offers

GET  /lenme/list-borrowers

GET  /lenme/list-borrowers/<int:pk>

GET  /lenme/list-borrowers/<int:pk>/loans

GET  /lenme/list-loans

GET  /lenme/list-loans/<int:pk>

GET  /lenme/list-loans/<int:pk>/offers

POST  /lenme/create-investor

POST  /lenme/create-borrower

POST  /lenme/create-loan

POST  /lenme/create-offer

POST  /lenme/accept-offer/<int:pk>/

POST  /lenme/make-single-payment/<int:pk>/
```

# examples

GET  "lenme/list-investors/<int:pk>/offers"

-Returns:
```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept


[
    {
        "id": 3,
        "investor": 1,
        "loan": 1,
        "interest": 15,
        "accepted": false,
        "created_at": "2021-01-30T09:59:02.691354Z"
    },
    {
        "id": 5,
        "investor": 1,
        "loan": 2,
        "interest": 15,
        "accepted": true,
        "created_at": "2021-01-30T10:06:33.075842Z"
    },
    {
        "id": 6,
        "investor": 1,
        "loan": 5,
        "interest": 16,
        "accepted": false,
        "created_at": "2021-01-30T10:30:14.290155Z"
    }
]
```

POST  "lenme/create-loan"

Request Arguments: Borrower, amount, period
example:
{"Borrower": 1, "amount": 5000, "period": 6}

-Returns:
```

HTTP 201 Created
Allow: OPTIONS, POST
Content-Type: application/json
Vary: Accept

{
    "id": 7,
    "Borrower": 1,
    "amount": 5000,
    "period": 6,
    "status": "Not funded",
    "paid_payments": 0,
    "created_at": "2021-01-30T15:53:21.741259Z",
    "updated_at": "2021-01-30T15:53:21.741302Z"
}
```


















    
    
