from time import sleep
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError


# Startup
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    # Copy and pasted this from stackoverflow, not sure why we import as _upgrade()
    from flask_migrate import upgrade as _upgrade
    # Retry database migrations for 10 seconds in case database is slow to start up
    # (Common in docker-compose environments)
    for _ in range(5):
        try:
            _upgrade()
            break
        except OperationalError as exc:
            sleep(2)

# Models
class Greeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    def __init__(self, text):
        self.text = text

# Api
@app.route('/')
def hello_world():
    return Greeting.query.first().text
