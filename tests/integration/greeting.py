import requests
import os

basepath = 'http://{}{}'.format(os.environ.get('APP_HOST'),os.environ.get('APP_PATH',''))

def test_home():
    "GET request to / returns a 200"
    resp = requests.get(basepath + '/')
    assert resp.status_code == 200

def test_nonexistent_greeting():
    resp = requests.get(basepath + '/5')
    print(resp.text)
    assert resp.status_code == 404

def test_create_greeting():
    new_greeting = {'text': 'I am a test greeting.'}
    resp = requests.post(basepath + '/newgreeting', json=new_greeting)
    assert resp.status_code == 201
    id = resp.json()['id']
    assert type(id) == int
    echoed_greeting = requests.get(basepath + '/' + str(resp.json()['id']))
    assert echoed_greeting.status_code == 200
    assert echoed_greeting.json()['text'] == new_greeting['text']
