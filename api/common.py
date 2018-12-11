from enum import Enum
from marshmallow import Schema, fields
from app import db, ma

class ErrorCode(Enum):
    SHORTCODE_NOTFOUND = 1
    SHORTCODE_RNG = 2
    INVALID_URL = 3
    DESERIALIZATION_FAIL = 4
    DUPLICATE_SHORTCODE = 5
 
class Error(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class ErrorSchema(Schema):
    code = fields.Int(required=True)
    message = fields.Str(required=True)

def error(code, message):
    return ErrorSchema().dump(Error(code.value, message)).data

class BaseSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session
