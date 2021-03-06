AISLES = ['dead animals', 'things wrapped in metal', 'bovine liquids', 'partially digested grains']

HAM_INGREDIENT = {
    'name': 'Ham',
    'aisleName': AISLES[0],
    'recipeUnit': 'lbs',
    'storeUnit': 'lbs',
    'unitConversion': 1,
    'storeUnitPrice': 2.25
}

BUN_INGREDIENT = {
    'name': 'Buns',
    'aisleName': AISLES[3],
    'recipeUnit': 'buns',
    'storeUnit': 'dozen',
    'unitConversion': 12,
    'storeUnitPrice': 3
}

CHEESE_INGREDIENT = {
    'name': 'cheddar',
    'aisleName': AISLES[2],
    'recipeUnit': 'oz',
    'storeUnit': 'lbs',
    'unitConversion': 16,
    'storeUnitPrice': 102
}

MILK_INGREDIENT = {
    'name': 'milk',
    'aisleName': AISLES[2],
    'recipeUnit': 'cups',
    'storeUnit': 'gallons',
    'unitConversion': 16,
    'storeUnitPrice': 2.1
}

INGREDIENTS = [HAM_INGREDIENT, BUN_INGREDIENT, MILK_INGREDIENT, CHEESE_INGREDIENT]

HAMMED_BURGER_RECIPE = {
    'name': 'hammed burger :(',
    'text': 'out of cheese what food',
    'source': 'https://i.redd.it/2xseyb4lq9a51.jpg',
    'servings': 6,
    'ingredients': [
        {'amount': 1.2, 'name': 'Ham'},
        {'amount': 0.5, 'name': 'Buns'},
    ]
}

MILK_SANDWICH_RECIPE = {
    'name': 'Milk Sandwich',
    'text': '<strike>you put the milk in the middle</strike>',
    'source': 'Catherine',
    'servings': 12.3,
    'ingredients': [
        {'amount': 3, 'name': 'Buns'},
        {'amount': 15, 'name': 'milk'}
    ]
}

HAM_SANDWICH_RECIPE = {
    'name': 'HAM SANDWICH',
    'text': 'HAM THE SANDWICH',
    'source': 'the void',
    'servings': 0.75,
    'ingredients': [
        {'amount': 1, 'name': 'Buns'},
        {'amount': 1, 'name': 'Ham'},
        {'amount': 1, 'name': 'cheddar'}
    ]
}

RECIPES = [HAMMED_BURGER_RECIPE, MILK_SANDWICH_RECIPE, HAM_SANDWICH_RECIPE]


ALPHONSE = {
    'name': 'Alphonse Blomenberg',
    'phone': '+1234567890',
    'email': 'cat@cat.com'
}

MARIPOSA = {
    'name': 'Mariposa Catto Skelton',
    'email': 'tripod@cat.com'
}

RECIPIENTS = [MARIPOSA, ALPHONSE]
