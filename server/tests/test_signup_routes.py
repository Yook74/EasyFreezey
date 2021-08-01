from datetime import date

from server.tests.fixtures import *


def test_post_simple(client):
    client.ensure_recipients_recipes_sessions()

    assert client.post('/signup', json=dict(
        recipientId=1,
        sessionId=1,
        recipeId=1,
        mealCount=2
    )).data == b'created signup'

    assert client.get_json('/session/1/recipe') == [dict(
        id=1, name='hammed burger :(', totalMeals=2
    )]

    assert client.get_json('/session/1') == dict(
        date=date.today().isoformat(),
        recipientNames=['Mariposa Catto Skelton']
    )


def test_post_empty(client):
    assert client.post('/signup', json={
        'recipientId': 1,
        'sessionId': 1,
        'recipeId': 1,
        'mealCount': 1,
    }).status_code == 404


def test_post_invalid_id(client):
    client.ensure_recipients_recipes_sessions()

    response = client.post('/signup', json={
        'recipientId': 10,
        'sessionId': 1,
        'recipeId': 1,
        'mealCount': 1,
    })
    assert response.status_code == 404
    assert response.data == b'404 Not Found: No recipient was found with the given ID'

    response = client.post('/signup', json={
        'recipientId': 1,
        'sessionId': 17,
        'recipeId': 1,
        'mealCount': 1,
    })
    assert response.status_code == 404
    assert response.data == b'404 Not Found: No session was found with the given ID'

    response = client.post('/signup', json={
        'recipientId': 1,
        'sessionId': 1,
        'recipeId': None,
        'mealCount': 1,
    })
    assert response.status_code == 404
    assert response.data == b'404 Not Found: No recipe was found with the given ID'

    assert client.get_json('/session/1')['recipientNames'] == []


def test_post_invalid_meal_count(client):
    client.ensure_recipients_recipes_sessions()

    response = client.post('/signup', json={
        'recipientId': 1,
        'sessionId': 1,
        'recipeId': 1,
        'mealCount': -4,
    })
    assert response.status_code == 400
    assert response.data == b'400 Bad Request: mealCount must be greater than or equal to 0'

    assert client.post('/signup', json={
        'recipientId': 1,
        'sessionId': 1,
        'recipeId': 1,
        'mealCount': 'beep beep',
    }).status_code == 400


def test_post_missing_key(client):
    client.ensure_recipients_recipes_sessions()

    response = client.post('/signup', json={})
    assert response.status_code == 400
    assert b'JSON was missing key' in response.data

    response = client.post('/signup', json={
        'recipientId': 1,
        'sessionId': 1,
        'recipeId': 1,
    })
    assert response.data == b'JSON was missing key "mealCount"'


'''Multiple posts tested in session routes'''
