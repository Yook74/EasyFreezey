from datetime import date, timedelta

from server.tests.fixtures import *
from server.tests.sample_data import *


def test_post_simple(client):
    client.ensure_aisles()

    assert client.post('/ingredient', json=dict(
        name='corn',
        aisleId=2,
        recipeUnit='cup',
        storeUnit='15 oz can',
        unitConversion=2,
        storeUnitPrice=.99
    )).data == b'1'

    assert client.get_json('/ingredient') == [{'id': 1, 'name': 'corn'}]


def test_post_missing_key(client):
    client.ensure_aisles()

    response = client.post('/ingredient', json={})
    assert response.status_code == 400
    assert b'JSON was missing key' in response.data

    response = client.post('/ingredient', json=dict(
        name='corn',
        aisleId=2,
        storeUnit='15 oz can',
        unitConversion=2,
        storeUnitPrice=.99
    ))
    assert response.status_code == 400
    assert response.data == b'JSON was missing key "recipeUnit"'


def test_post_invalid_id(client):
    client.ensure_aisles()

    response = client.post('/ingredient', json=dict(
        name='corn',
        aisleId=8,
        recipeUnit='cup',
        storeUnit='15 oz can',
        unitConversion=2,
        storeUnitPrice=.99
    ))
    assert response.status_code == 404
    assert response.data == b'404 Not Found: No Aisle was found with that ID'


def test_post_invalid_types(client):
    client.ensure_aisles()

    assert client.post('/ingredient', json=dict(
        name='corn',
        aisleId='snail',
        recipeUnit='cup',
        storeUnit='15 oz can',
        unitConversion=2,
        storeUnitPrice=.99
    )).status_code == 400

    assert client.post('/ingredient', json=dict(
        name='corn',
        aisleId=2,
        recipeUnit='cup',
        storeUnit='15 oz can',
        unitConversion=None,
        storeUnitPrice=.99
    )).status_code == 400

    assert client.post('/ingredient', json=dict(
        name='corn',
        aisleId=2,
        recipeUnit='cup',
        storeUnit='15 oz can',
        unitConversion=2,
        storeUnitPrice='$0.99'
    )).status_code == 400

    assert client.get_json('/ingredient') == []


def test_post_multiple(client):
    client.ensure_aisles()

    ingredients = [dict(
        name='Canned Corn',
        aisleId=2,
        aisle='things wrapped in metal',
        recipeUnit='cups',
        storeUnit='15 oz can',
        unitConversion=2,
        storeUnitPrice=.99
    ), dict(
        name='Chonk Chicken$!<wib>',
        aisleId=1,
        aisle='dead animals',
        recipeUnit='oz',
        storeUnit='12 oz can',
        unitConversion=12,
        storeUnitPrice=1.25
    ), dict(
        name='an entire buffalo',
        aisleId=1,
        aisle='dead animals',
        recipeUnit='lb',
        storeUnit='buffalo',
        unitConversion=2000,
        storeUnitPrice=1999
    )]

    for ingredient in ingredients:
        client.post('/ingredient', json=ingredient)
        del ingredient['aisleId']

    for index, ingredient in enumerate(ingredients):
        assert client.get_json(f'/ingredient/{index + 1}') == ingredient


def test_get_empty(client):
    assert client.get_json('/ingredient') == []
    assert client.get('/ingredient/1').status_code == 404


def test_get_invalid(client):
    client.ensure_aisles()
    client.ensure_ingredients()

    assert client.get('/ingredient/5').status_code == 404
