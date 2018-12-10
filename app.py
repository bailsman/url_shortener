from time import sleep
import os
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import OperationalError
import connexion

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

connex_app = connexion.App(__name__, specification_dir='./api/')
app = connex_app.app
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
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
connex_app.add_api('openapi.yml', validate_responses=True)

@app.route('/')
def swagger_ui():
    return redirect('/ui')
