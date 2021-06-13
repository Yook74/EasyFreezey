import os
import tempfile
import json
import time
from datetime import date, timedelta

from copy import deepcopy
import pytest
from werkzeug.test import Client

from server.app import create_app, db
from server.tests.sample_data import *


class TestClientWrapper:
    """Provides all the methods of a werkzeug test client with a few extra convenience methods"""
    def __init__(self, test_client: Client):
        self.test_client = test_client

    def __getattr__(self, item):
        """
        If someone tries to access an attribute (including methods) of this instance that we don't know about
        try accessing that attribute on the test client.
        """
        return self.test_client.__getattribute__(item)

    def get_json(self, path: str) -> dict:
        response = self.test_client.get(path)
        return json.loads(response.data)

    def ensure_aisles(self, aisles=AISLES):
        """
        Creates the given aisles if they do not already exist
        and then returns all the aisles in the database
        """
        existing_aisle_names = [aisle['name'] for aisle in self.get_json('/aisle')]

        for aisle_name in aisles:
            if aisle_name not in existing_aisle_names:
                self.post('/aisle', json={'name': aisle_name})

        return self.get_json('/aisle')

    def ensure_ingredients(self, ingredients=INGREDIENTS):
        """
        Creates the given ingredients if they do not already exist
        and returns all the ingredients in the database
        """
        self.ensure_aisles()

        existing_ingredient_names = [ingredient['name'] for ingredient in self.get_json('/ingredient')]
        aisle_ids = {aisle['name']: aisle['id'] for aisle in self.get_json('/aisle')}

        for ingredient in deepcopy(ingredients):
            ingredient['aisleId'] = aisle_ids[ingredient['aisleName']]  # set the ID based on the name

            if ingredient['name'] not in existing_ingredient_names:
                self.post('/ingredient', json=ingredient)

        return self.get_json('/ingredient')

    def ensure_recipes(self, recipes=RECIPES):
        """
        Creates the given recipes if they do not already exist
        and returns all the recipes in the database
        """
        self.ensure_ingredients()

        existing_recipe_names = [recipe['name'] for recipe in self.get_json('/recipe')]
        ingredient_ids = {ingredient['name']: ingredient['id'] for ingredient in self.get_json('/ingredient')}

        for recipe in deepcopy(recipes):
            for ingredient in recipe['ingredients']:
                ingredient['id'] = ingredient_ids[ingredient['name']] # set the ID based on the name

            if recipe['name'] not in existing_recipe_names:
                self.post('/recipe', json=recipe)

        return self.get_json('/recipe')

    def ensure_recipients(self, recipients=RECIPIENTS):
        """Creates the given recipients if they do not already exist"""
        for recipient in recipients:
            self.post('/recipient', json=recipient)

    def ensure_recipients_recipes_sessions(self):
        self.ensure_recipes()
        self.ensure_recipients()

        self.post('/session', json={'date': date.today().isoformat()})
        self.post('/session', json={'date': (date.today() + timedelta(weeks=1)).isoformat()})


@pytest.fixture()
def client():
    db_file_handle, db_file_path = tempfile.mkstemp()

    app = create_app()
    app.testing = True

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
    with app.app_context():
        db.create_all()

    test_client = TestClientWrapper(app.test_client())
    yield test_client
    del test_client

    os.unlink(db_file_path)
    os.close(db_file_handle)
