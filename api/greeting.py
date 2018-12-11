from app import db, ma
from api.common import Error, ErrorSchema

class Greeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    def __init__(self, text):
        self.text = text

class GreetingSchema(ma.ModelSchema):
    class Meta:
        model = Greeting
        sqla_session = db.session

def get(id):
    greeting = Greeting.query.get(id)
    if greeting is None:
        return ErrorSchema().dump(Error(1, 'Specified greeting not found.')).data, 404
    return GreetingSchema().dump(greeting).data

def create(body):
    schema = GreetingSchema()
    new_greeting = schema.load(body, session=db.session).data
    db.session.add(new_greeting)
    db.session.commit()
    data = schema.dump(new_greeting).data
    return data, 201
