## Parking System

Parking System API to manage car parking in mall. Handles fee calculation and provides endpoint make payment.

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

## Testing
To run the tests for the app, and see the coverage, run
```
python manage.py test
```