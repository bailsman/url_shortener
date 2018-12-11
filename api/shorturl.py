import random
import string
from app import db, ma
from api.common import error, ErrorCode, BaseSchema
from datetime import datetime
from flask import redirect as flaskRedirect
from sqlalchemy.exc import IntegrityError

SHORTCODE_LENGTH = 6

class Shorturl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortcode = db.Column(db.String(SHORTCODE_LENGTH), unique=True, nullable=False)
    url = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lastRedirect = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    redirectCount = db.Column(db.Integer, default=0)

class ShorturlSchema(BaseSchema):
    url = ma.URL(load_only=True, required=True)
    shortcode = ma.String(missing=None)
    class Meta:
        model = Shorturl
        fields = ('url', 'shortcode')

class ShorturlStatsSchema(BaseSchema):
    class Meta:
        model = Shorturl
        fields = ('created', 'lastRedirect', 'redirectCount')

def random_shortcode():
    return ''.join(random.choices(string.ascii_letters + string.digits + '_', k=SHORTCODE_LENGTH))


def stats(shortcode):
    shorturl = Shorturl.query.filter(Shorturl.shortcode == shortcode).one_or_none()
    if shorturl is None:
        return error(ErrorCode.SHORTCODE_NOTFOUND, 'Shortcode not found.'), 404
    return ShorturlStatsSchema().dump(shorturl).data

def redirect(shortcode):
    shorturl = Shorturl.query.filter(Shorturl.shortcode == shortcode).one_or_none()
    if shorturl is None:
        return error(ErrorCode.SHORTCODE_NOTFOUND, 'Shortcode not found.'), 404
    shorturl.redirectCount = Shorturl.redirectCount + 1
    shorturl.lastRedirect = datetime.utcnow()
    db.session.commit()
    return flaskRedirect(shorturl.url)

def create(body):
    schema = ShorturlSchema()
    new_shorturl = schema.load(body).data
    if not isinstance(new_shorturl, Shorturl):
        if 'url' not in new_shorturl:
            return error(ErrorCode.INVALID_URL, 'Could not process URL. Make sure scheme and tld are present.'), 422
        else:
            return error(ErrorCode.DESERIALIZATION_FAIL, 'Deserialization failed due to an internal error. Contact the server administrator.'), 500
    if new_shorturl.shortcode is None:
        max_tries = 3
        for i in range(max_tries):
            # Try a couple of times in case we get unlucky and our random code already exists
            try:
                new_shorturl.shortcode = random_shortcode()
                db.session.add(new_shorturl)
                db.session.commit()
            except IntegrityError:
                if i == max_tries - 1:
                    raise
    else:
        # User supplied a shortcode, so just bubble up the error if it is a duplicate
        try:
            db.session.add(new_shorturl)
            db.session.commit()
        except IntegrityError:
            # This just assumes all instances if IntegrityError
            # are "Violates unique shortcode constraint"
            # which means we are relying on good validation before we get here
            return error(ErrorCode.DUPLICATE_SHORTCODE, 'Shortcode already in use'), 409
    data = schema.dump(new_shorturl).data
    return data, 201
