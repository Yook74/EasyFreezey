from datetime import date, timedelta

from src.tests.fixtures import *
from src.tests.sample_data import *


def test_get_session_recipe(client):
    assert client.get('/1/recipe').status_code == 404

    client.post('/session', json={'date': date.today().isoformat()})
    assert client.get_json('/1/recipe') == []

    client.ensure_recipes()
    client.ensure_recipients()
    client.post('/signup', json={'sessionId': 1, 'recipeId': 1, 'recipientId': 1, 'mealCount': 2})
    assert client.get_json('/1/recipe') == [{'id': 1, 'name': 'hammed burger :(', 'totalMeals': 2.0}]

    client.post('/session', json={'date': (date.today() + timedelta(weeks=1)).isoformat()})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 1, 'recipientId': 2, 'mealCount': 3.5})
    client.post('/signup', json={'sessionId': 1, 'recipeId': 2, 'recipientId': 2, 'mealCount': 1})
    client.post('/signup', json={'sessionId': 2, 'recipeId': 2, 'recipientId': 1, 'mealCount': 2.3})
    client.post('/signup', json={'sessionId': 2, 'recipeId': 2, 'recipientId': 2, 'mealCount': 1.1})

    assert client.get_json('/1/recipe') == [
        {'id': 1, 'name': 'hammed burger :(', 'totalMeals': 5.5},
        {'id': 2, 'name': 'Milk Sandwich', 'totalMeals': 1}
    ]
    assert client.get_json('/2/recipe') == [{'id': 2, 'name': 'Milk Sandwich', 'totalMeals': 3.4}]


def test_shopping_list(client):
    assert client.get('/1/shopping').status_code == 404

    client.post('/session', json={'date': date.today().isoformat()})
    assert client.get_json('/1/shopping') == []
