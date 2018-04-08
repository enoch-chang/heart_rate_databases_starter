# heart_rate_databases_starter
This is the back-end component of a heart rate monitor, consisting of the server and the database. 

The server component ```webservice.py``` is a Flask application that allows users to add heart rate data to a specified user, retrieve all the heart rate from a specified user, retrieve the average heart rate for the specified user and to retrieve the average heart rate over a specified time frame for a specified user.

The database component ```main.py``` stores and retrieves information from a MongoDB database. It can add heart rate information to an existing user, create new users, retrieve user information and retrieve all heart rate information stored for a specified user. All information is stored in the format specified in ```models.py```.

## Installation and Deployment

To get started, you first need to install required python packages into your virtual environment.
```
pip install -r requirements.txt
```

### To run on a virtual machine
This code is to be deployed from a virtual machine. First, the database is initiated. MongoDB can be run using ```Docker``` by running the following command once installed into your virtual machine:
```
sudo docker run -v $PWD/db:/data/db -p 27017:27017 mongo
```

To run the server, execute using ```gunicorn```:
```
gunicorn --bind 0.0.0.0:5000 webservice:app
```	

### To run locally
To deploy locally, modify the address of the associated database in line 18 of ```webservice.py``` to:
```
connect("mongodb://localhost:27017/bme590")
```

MongoDB can be run using ```Docker``` by running the following command once installed:
```
docker run -v $PWD/db:/data/db -p 27017:27017 mongo
```

To run the server, execute using the following script:
```
FLASK_APP=webservice.py flask run
```	

Travis CI Status:  [![Build Status](https://travis-ci.org/enoch-chang/bme590hrm.svg?branch=master)](https://travis-ci.org/enoch-chang/bme590hrm)
