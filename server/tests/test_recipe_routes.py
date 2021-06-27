from server.tests.fixtures import *
from server.tests.sample_data import *


def test_post_missing_key(client):
    client.ensure_ingredients()

    response = client.post('/recipe', json={})
    assert response.status_code == 400
    assert b'JSON was missing key' in response.data

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
    ))
    assert response.status_code == 400
    assert response.data == b'JSON was missing key "ingredients"'

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': 1}]
    ))
    assert response.status_code == 400
    assert response.data == b'JSON was missing key "amount"'


def test_post_invalid_ingredient(client):
    client.ensure_ingredients()

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[]
    ))
    assert response.status_code == 400
    assert response.data == b'400 Bad Request: Recipes must have at least one ingredient'

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': 1, 'amount': 1}, {'id': 1, 'amount': 2}]
    ))
    assert response.status_code == 400

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': 1, 'amount': -1}]
    ))
    assert response.status_code == 400
    assert response.data == b'400 Bad Request: Recipe amounts must be greater than 0'

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': 500, 'amount': 0.2}]
    ))
    assert response.status_code == 404
    assert response.data == b'404 Not Found: No ingredient with id 500 was found'


def test_post_duplicate(client):
    client.ensure_recipes()
    assert client.post('/recipe', json=dict(
        name='Milk Sandwich',
        text='text',
        source='Source',
        servings=1,
        ingredients=[{'id': 1, 'amount': 1}]
    )).status_code == 400


def test_post_invalid(client):
    client.ensure_ingredients()

    response = client.post('/recipe', json=dict(
        name=None,
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': 1, 'amount': 0.2}]
    ))
    assert response.status_code == 400

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=-1,
        ingredients=[{'id': 1, 'amount': 0.2}]
    ))
    assert response.status_code == 400
    assert response.data == b'400 Bad Request: The recipe must have a positive number of servings'

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': None, 'amount': 0.2}]
    ))
    assert 400 <= response.status_code < 500

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=None,
        ingredients=[{'id': 1, 'amount': 0.2}]
    ))
    assert response.status_code == 400
    assert response.data == b'400 Bad Request: Invalid type in JSON'

    assert client.get_json('/recipe') == []


def test_post_simple(client):
    client.ensure_ingredients()

    response = client.post('/recipe', json=dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[{'id': 1, 'amount': 0.2}]
    ))
    assert response.data == b'1'
    assert response.status_code == 200

    assert client.get_json('/recipe/1') == dict(
        name='Name',
        text='Text',
        source='Source',
        servings=1,
        ingredients=[dict(
            id=1,
            name='Ham',
            amount=0.2,
            unit='lbs'
        )]
    )


def test_post_get_multiple(client):
    client.ensure_ingredients()

    recipes = [dict(
        name='<strong>Glass of milk</strong>',
        text='<em>Spill it</em>',
        source='https://example.com',
        servings=1,
        ingredients=[dict(
            id=3,
            amount=2.2,
            name='milk',
            unit='cups'
        )]
    ), dict(
        name='Name',
        text='Very large text' * 1000,
        source='Charles Entertainment Cheese',
        servings=4.12,
        ingredients=[dict(
            id=2,
            amount=5,
            name='Buns',
            unit='buns'
        )]
    ), dict(
        name='Nameee',
        text='Text',
        source='Source',
        servings=.1,
        ingredients=[dict(
            id=1,
            amount=1.2,
            name='Ham',
            unit='lbs'
        ), dict(
            id=2,
            amount=3,
            name='Buns',
            unit='buns'
        ), dict(
            id=3,
            amount=4,
            name='milk',
            unit='cups'
        )]
    )]

    for recipe in recipes:
        assert client.post('/recipe', json=recipe).status_code == 200

    for index, recipe in enumerate(recipes):
        assert client.get_json(f'/recipe/{index + 1}') == recipe


def test_get_empty(client):
    assert client.get_json('/recipe') == []
    assert client.get('/recipe/1').status_code == 404


def test_get_invalid(client):
    client.ensure_recipes()
    assert client.get('/recipe/20').status_code == 404
