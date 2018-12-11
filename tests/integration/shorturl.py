import os
from datetime import datetime, timedelta, timezone
import requests

basepath = 'http://{}{}'.format(os.environ.get('APP_HOST'),os.environ.get('APP_PATH',''))

def test_home():
    resp = requests.get(basepath + '/')
    assert resp.status_code == 200

def test_invalid_shortcode():
    resp = requests.post(basepath + '/shorten', json={
      'url': 'http://example.com',
      'shortcode': '@#*!&'
    })
    assert resp.status_code == 400

def test_valid_flow():
    resp = requests.post(basepath + '/shorten', json={
        'url': 'http://example.com',
        'shortcode': 'valido'
    })
    assert resp.status_code == 201
    shortcode = resp.json()['shortcode']

    resp = requests.get(basepath + '/' + shortcode, allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers['Location'] == 'http://example.com'

    resp = requests.get(basepath + '/' + shortcode + '/stats')
    now = datetime.now(timezone.utc)
    fiveminutes = timedelta(minutes=5) # Make sure clock drift does not cause flaking
    created = datetime.fromisoformat(resp.json()['created'])
    lastRedirect = datetime.fromisoformat(resp.json()['lastRedirect'])
    assert now - created < fiveminutes
    assert lastRedirect - now < fiveminutes
    assert resp.json()['redirectCount'] == 1 

    # Redirect again so we can test lastRedirect update and redirectCount increment
    resp = requests.get(basepath + '/' + shortcode, allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers['Location'] == 'http://example.com'

    resp = requests.get(basepath + '/' + shortcode + '/stats')
    assert resp.json()['redirectCount'] == 2
    assert datetime.fromisoformat(resp.json()['lastRedirect']) > lastRedirect
