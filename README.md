## Parking System

Parking System API to manage car parking in malls. Handles fee calculation and provides endpoint to make payment.

## Installation
Clone the repo
```
clone with ssh, use
git clone git@github.com:malikwahab/parking-system.git

# clone with https, use
git clone https://github.com/malikwahab/parking-system.git
```
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

 ```sh
$ cd parking-system
$ virtualenv -p python3.6 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
 ```
 If you are on Windows, then use the following commands instead:

 ```sh
$ virtualenv -p python3 venv
$ venv\Scripts\activate
(venv) $ pip install -r requirements.txt
```

## Perform migrations
```
python manage.py migrate
```

## Start Server
```
python manage.py runserver
```

## Testing
To run the tests for the app, and see the coverage, run
```
python manage.py test
```

## Usage

This Application uses browsable API. To get started visit the home url

#### API schema
Get a swagger documentation of the API

```
GET /schema
```

#### Create a mall
```
POST /mall

{
  "name": "string",
  "maximum_no_cars": 0,
  "tenants": [
    "string"
  ]
}
```

#### Get all malls

```
GET /mall
```

#### Get a mall

```
GET /mall/{id}
```

#### Edit a mall

```
PUT /mall/{id}

{
  "name": "string",
  "maximum_no_cars": 0,
  "tenants": [
    "string"
  ]
}
```

#### Delete a mall

```
DELETE /mall/{id}
```

#### Get mall payment details

Retrive the fee paid and the outstanding ticket fees
This endpoint accept a query param `days` that specify the number of days back to get payment for, if not specified, the all time payment details will be returned
```
GET /mall/{mall_id}/payment-details?days=1
```

#### Get all parking tickets in a mall

```
GET /mall/{mall_pk}/parkingtickets/
```

#### Create a parking ticket

```
POST /mall/{mall_pk}/parkingtickets/

{
  "plate_number": "string",
  "mall": "string",
  "tenant": "string"
}

```

#### Get a parking ticket

```
GET /mall/{mall_pk}/parkingtickets/{id}/
```

#### Edit a parking ticket

```
PUT /mall/{mall_pk}/parkingtickets/{id}/

{
  "plate_number": "string",
  "mall": "string",
  "tenant": "string"
}

```

#### Delete a parking ticket

```
DELETE /mall/{mall_pk}/parkingtickets/{id}/
```

#### Make payment for a parking ticket

```
POST /pay-ticket/{ticket_id}/
{
    "fee_paid": 0
}
```

#### Exit a park
Successful if all payment has been made, fail otherwise

```
GET /exit/{ticket_id}/
```

#### Create a tenant
```
POST /mall/{mall_pk}/tenants/

{
  "name": "string",
  "malls": [
    "string"
  ]
}

```

#### Get all tenants
```
GET /mall/{mall_pk}/tenants/
```

#### Get a tenant
```
GET /mall/{mall_pk}/tenants/{id}
```

#### Edit a tenant
```
PUT /mall/{mall_pk}/tenants/{id}/
```

#### Delete a tenant
```
DELETE /mall/{mall_pk}/tenants/{id}/
```