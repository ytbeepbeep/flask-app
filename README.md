# flask-app
_Interact with our microservices architecture_

[![Build Status](https://travis-ci.org/ytbeepbeep/flask-app.svg?branch=master)](https://travis-ci.org/ytbeepbeep/flask-app)
[![Coverage Status](https://coveralls.io/repos/github/ytbeepbeep/flask-app/badge.svg?branch=master)](https://coveralls.io/github/ytbeepbeep/flask-app?branch=master)

_This microservice works on port 5001._

## First setup
Export the address and the port of the [data-service](https://github.com/ytbeepbeep/data-service) microservice,
the default is `127.0.0.1:5002`.

A smart way to do this is to create a file `variables.sh` in the project root, as follows.
```
#!/bin/bash
export DATA_SERVICE="127.0.0.1:5002"
```
You can load the variables with `source variables.sh`.

#### Install for development
```
pip install -r requirements.txt
pip install pytest pytest-cov
python setup.py develop
```

#### Install for production
```
pip install -r requirements.txt
python setup.py install
```


## Run the microservice

##### Terminal #1
Start the [data-service](https://github.com/ytbeepbeep/data-service) microservice.

##### Terminal #2
1. Load environment variables:  
   `source variables.sh`

2. Start with:  
   `python flaskapp/app.py`


## Docker
[![Image size](https://images.microbadger.com/badges/image/ytbeepbeep/flask-app.svg)](https://microbadger.com/images/ytbeepbeep/flask-app)
[![Latest version](https://images.microbadger.com/badges/version/ytbeepbeep/flask-app.svg)](https://microbadger.com/images/ytbeepbeep/flask-app)

A Docker Image is available on the public Docker Hub registry. You can run it with the command below.
- Run the [data-service](https://github.com/ytbeepbeep/data-service#docker) container
- Run mail-service with `docker run -d --name flask-app -e DATA_SERVICE="data-service:5002"
--link data-service:data-service ytbeepbeep/flask-app`

**Important note:** if the `data-service` container is running on another Docker installation,
replace `data-service` with the host, as follows: `-e DATA_SERVICE="<myhost-name-or-address>:5002"`

#### Locally
You can also build your own image from this repository.
- Build with `docker build -t ytbeepbeep/flask-app .`
- Run as usually, with the commands specified above
