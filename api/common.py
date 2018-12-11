from marshmallow import Schema, fields

class Error(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class ErrorSchema(Schema):
    code = fields.Int()
    message = fields.Str()

