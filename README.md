# What is this?

This is a toy project for me to learn how to make apis in Python with Flask. It implements a very basic url shortener app.
Almost all files in the repo are boilerplate, the code that actually does anything is in api/ and tests/

Tools used:

* flask
* gunicorn
* psycopg2
* Flask-SQLAlchemy
    + Our standard ORM in python. I wanted to test on a postgresql db rather than sqlite, since I imagine most production apps will eventually run on something like postgresql.
* Flask-Migrate
    + Even though I only have one "migration" - which sets up my one table, I included this because I wanted to see how migrations work in Flask.
* Flask-Marshmallow
* marshmallow-sqlalchemy
    + Marshmallow seems to be a very solid serialization library to convert between your datastore and your JSON consumers. It does some validation out of the box (used in this app to validate URLs, for example) and the sqlalchemy integration makes it very simple to (de)serialize with little effort and high code clarity. I believe this is commonly used nowadays.
* connexion[swagger-ui]
    + I'm glad I stumbled onto this neat little Flask plugin by Zalando - it routes requests based on your openapi.yml and can validate both requests and responses. Great to keep your code in sync with your spec and documentation. This way you get a lot validation and documentation basically for free.
* pytest-flask-sqlalchemy
    + Transaction based rollback for test isolation. Makes it easy to test against real postgresql without having to reset the database every test.

# How to run

With docker and docker-compose installed, run `docker-compose up` and navigate to http://localhost:5000/ to get swagger ui as interactive documentation.

# How to run the tests

Again with docker and docker-compose installed `./runtests` runs both unit and integration tests.

# Production use

Needless to say as a toy project this is not suitable to run in production in any capacity. At the very least you'd want to put nginx in front of it so as not to expose gunicorn directly to clients, and perhaps use something like haproxy's stick tables to counteract bruteforcing short codes.
