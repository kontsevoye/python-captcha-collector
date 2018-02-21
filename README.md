# python-captcha-collector

This project created for collecting and checking captcha images from http://iq.karelia.ru 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

First of all you need a python3 with pip

```
# dnf install python3 python3-pip
```

For next you will need virtualenv

```
# pip3 install virtualenv
```

### Installing

A step by step series of examples that tell you have to get a development env running

Copy repository to a local machine and cd into it

```
git clone https://github.com/instane/python-captcha-collector.git && cd python-captcha-collector
```

Create virtual environment

```
virtualenv -p python3 venv3
```

Install requirement libraries

```
venv3/bin/pip install -r requirements.txt
```

Make your .env file with configurations

```
cp .env.example .env
```

Now you can run web server in production mode

```
FLASK_APP=pcc.py venv3/bin/flask run
```

Or in debug mode

```
FLASK_APP=pcc.py FLASK_DEBUG=1 venv3/bin/flask run
```

After all you cann access this app through browser. By default it run on http://127.0.0.1:5000/ 

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Requests](http://docs.python-requests.org/en/master/) - HTTP request library

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/instane/python-captcha-collector/tags). 

## Authors

* **Evgeny** - *Initial work* - [instane](https://github.com/instane)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

