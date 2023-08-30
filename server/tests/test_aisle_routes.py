from server.tests.fixtures import *
from server.tests.sample_data import *


def test_get_empty(client):
    assert client.get_json('/aisle') == []


def test_post_get_simple(client):
    assert client.post('/aisle', json={'name': 'cheese'}).data == b'1'

    assert client.get_json('/aisle') == [{
        'name': 'cheese', 'id': 1
    }]


def test_post_get_multiple(client):
    assert client.post('/aisle', json={'name': 'cheese'}).data == b'1'
    assert client.post('/aisle', json={'name': 'lego'}).data == b'2'
    assert client.post('/aisle', json={'name': 'bees'}).data == b'3'

    assert client.get_json('/aisle') == [
        {'name': 'cheese', 'id': 1},
        {'name': 'lego', 'id': 2},
        {'name': 'bees', 'id': 3}
    ]


def test_post_invalid(client):
    assert client.post('/aisle', json={'name': None}).status_code == 400
    assert client.post('/aisle', json={'feet': None}).status_code == 400
    assert client.post('/aisle', json={}).status_code == 400

    assert client.get_json('/aisle') == []


def test_post_aisle_naming(client):
    assert client.post('/aisle', json={'name': 'abcdefg'}).status_code == 200
    assert client.post('/aisle', json={'name': 'abcdef'}).status_code == 400
    assert client.post('/aisle', json={'name': 'abcDeFg'}).status_code == 400
    assert client.post('/aisle', json={'name': 'abc def'}).status_code == 400
    assert client.post('/aisle', json={'name': 'abcdef part 2'}).status_code == 200



