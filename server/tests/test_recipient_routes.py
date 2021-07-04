from server.tests.fixtures import *


def test_get_empty(client):
    assert client.get_json('/recipient') == []


def test_post_simple(client):
    assert client.post('/recipient', json={
        'name': 'Puddles Issler',
        'email': 'twisttielover@cat.com',
        'phone': '123456789'
    }).data == b'1'

    assert client.get_json('/recipient') == [{
        'name': 'Puddles Issler',
        'email': 'twisttielover@cat.com',
        'phone': '123456789'
    }]


def test_multiple(client):
    assert client.post('/recipient', json={
        'name': 'Midnight',
        'email': 'pipecleanerlover@cat.com',
        'phone': None
    }).data == b'1'

    assert client.post('/recipient', json={
        'name': 'Puddles Issler',
        'phone': '+1 (123) 456-7890',
    }).data == b'2'

    assert client.post('/recipient', json={
        'name': 'Mariposa Skelton',
    }).data == b'3'

    assert client.get_json('/recipient') == [
        {
            'name': 'Midnight',
            'phone': None,
            'email': 'pipecleanerlover@cat.com'
        }, {
            'name': 'Puddles Issler',
            'phone': '+1 (123) 456-7890',
            'email': None,
        }, {
            'name': 'Mariposa Skelton',
            'phone': None,
            'email': None,
    }]


def test_post_invalid(client):
    assert client.post('/recipient', json={}).status_code == 400

    assert client.post('/recipient', json={
        'snail': 'beep'
    }).status_code == 400

    assert client.get_json('/recipient') == []


