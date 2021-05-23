from datetime import date, timedelta

from src.tests.fixtures import *
from src.tests.sample_data import *


def test_get_session_recipes_empty(client):
    assert client.get('/session/1/recipe').status_code == 404

    client.post('/session', json={'date': date.today().isoformat()})
    assert client.get_json('/session/1/recipe') == []


def test_get_session_recipes_one_signup(client):
    client.ensure_recipes()
    client.ensure_recipients()
    client.post('/session', json={'date': date.today().isoformat()})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 1, 'recipientId': 1, 'mealCount': 2})

    assert client.get_json('/session/1/recipe') == [{'id': 1, 'name': 'hammed burger :(', 'totalMeals': 2.0}]


def test_get_session_recipes_multiple_signups(client):
    client.ensure_recipes()
    client.ensure_recipients()

    client.post('/session', json={'date': date.today().isoformat()})
    client.post('/session', json={'date': (date.today() + timedelta(weeks=1)).isoformat()})

    client.post('/signup', json={'sessionId': 1, 'recipeId': 1, 'recipientId': 1, 'mealCount': 2})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 1, 'recipientId': 2, 'mealCount': 3.5})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 2, 'recipientId': 2, 'mealCount': 1})
    client.post('/signup', json={'sessionId': 2, 'recipeId': 2, 'recipientId': 1, 'mealCount': 2.3})
    client.post('/signup', json={'sessionId': 2, 'recipeId': 2, 'recipientId': 2, 'mealCount': 1.1})

    assert client.get_json('/session/1/recipe') == [
        {'id': 1, 'name': 'hammed burger :(', 'totalMeals': 5.5},
        {'id': 2, 'name': 'Milk Sandwich', 'totalMeals': 1}
    ]
    assert client.get_json('/session/2/recipe') == [{'id': 2, 'name': 'Milk Sandwich', 'totalMeals': 3.4}]


def test_shopping_list_empty(client):
    assert client.get('/session/1/shopping').status_code == 404

    client.post('/session', json={'date': date.today().isoformat()})
    assert client.get_json('/session/1/shopping') == []


def test_shopping_list_one_signup(client):
    client.ensure_recipes()
    client.ensure_recipients()

    client.post('/session', json={'date': date.today().isoformat()})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 2, 'recipientId': 2, 'mealCount': 1.5})

    assert client.get_json('/session/1/shopping') == [
        {'name': 'milk', 'unit': 'gallons', 'aisle': 'bovine liquids', 'qty': 1.40625},
        {'name': 'Buns', 'unit': 'dozen', 'aisle': 'partially digested grains', 'qty': .375},
    ]


def test_shopping_list_multiple_signups(client):
    client.ensure_recipes()
    client.ensure_recipients()

    client.post('/session', json={'date': date.today().isoformat()})
    client.post('/session', json={'date': (date.today() + timedelta(weeks=1)).isoformat()})

    client.post('/signup', json={'sessionId': 1, 'recipeId': 2, 'recipientId': 2, 'mealCount': 1.5})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 1, 'recipientId': 1, 'mealCount': 1.5})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 2, 'recipientId': 1, 'mealCount': 1})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 3, 'recipientId': 1, 'mealCount': 5})
    client.post('/signup', json={'sessionId': 2, 'recipeId': 1, 'recipientId': 1, 'mealCount': 2.3})
    client.post('/signup', json={'sessionId': 2, 'recipeId': 1, 'recipientId': 2, 'mealCount': 1.1})

    assert client.get_json('/session/1/shopping') == [
        {'name': 'Ham', 'unit': 'lbs', 'aisle': 'dead animals', 'qty': 6.8},
        {'name': 'milk', 'unit': 'gallons', 'aisle': 'bovine liquids', 'qty': 2.34375},
        {'name': 'cheddar', 'unit': 'lbs', 'aisle': 'bovine liquids', 'qty': 0.3125},
        {'name': 'Buns', 'unit': 'dozen', 'aisle': 'partially digested grains', 'qty': 1.1041666666666667},
    ]

    assert client.get_json('/session/2/shopping') == [
        {'name': 'Ham', 'unit': 'lbs', 'aisle': 'dead animals', 'qty': 4.08},
        {'name': 'Buns', 'unit': 'dozen', 'aisle': 'partially digested grains', 'qty': 0.14166666666666666},
    ]
