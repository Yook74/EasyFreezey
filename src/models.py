from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Ingredient(db.Model):
    """
    Ingredients have a many-to-many relationship with Recipes,
    which means any two recipes must call for ingredients in the same units.
    For example, one recipe cannot call for 1/3 of a cup of soy sauce while another calls for 2 tablespoons.
    In this example, both would need to call for a number of cups or a number of tablespoons.

    recipe_unit is the unit used in a recipe e.g. "tsp" where store_unit is the unit that one might find in a store.
    For example, store_unit might be "1.8 oz jar" for a spice.
    unit_conversion converts from recipe_unit to store_unit. Usually this is greater than or equal to 1
    store_unit price is the cost of one store_unit wherever the shopping will be done; usually Costco.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    aisle_id = db.Column(db.Integer(), db.ForeignKey('aisle.id'))
    recipe_unit = db.Column(db.String(32), nullable=False)
    store_unit = db.Column(db.String(32), nullable=False)
    unit_conversion = db.Column(db.Float(), nullable=False)
    store_unit_price = db.Column(db.Float(), nullable=False)

    aisle = db.relationship('Aisle', backref='recipes')


class Aisle(db.Model):
    """
    Represents an abstract section of a store.
    For example, Canned Goods
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)


class Recipe(db.Model):
    """
    Represents a single variant of a recipe.
    If the user wants to add a version of a recipe that is gluten free, for example,
    they will need to add another row to this table

    The text column stores the text of the recipe as a HTML string.
    The source may be a url or simply a description like "Grandma B."
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text(), nullable=True)
    source = db.Column(db.String(256), nullable=True)
    servings = db.Column(db.Float(), nullable=False)

    @property
    def cost(self) -> float:
        """The total cost of all the ingredients in this recipe"""
        return sum([
            recipe_ingredient.cost for recipe_ingredient in RecipeIngredient.query.filter_by(recipe_id=self.id)
        ])


class RecipeIngredient(db.Model):
    """
    Serves to associate recipes with ingredients, and indicates an amount of the ingredient in a recipe.
    Amount is in units of ingredient.recipe_unit.
    """
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer(), db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Float(), nullable=False)

    ingredient = db.relationship('Ingredient')
    recipe = db.relationship('Recipe')

    @property
    def cost(self) -> float:
        """:return: The cost of this ingredient in this recipe"""
        return (self.ingredient.store_unit_price / self.ingredient.unit_conversion) * self.amount


class Tag(db.Model):
    """
    Makes it easier to search for recipes.
    color is a hex color.
    """
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(64), nullable=False)
    color = db.Column(db.String(8), nullable=True)


class RecipeTag(db.Model):
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'), primary_key=True)
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'), primary_key=True)


class Session(db.Model):
    """A session is an event when meal prep is performed."""
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False, unique=True)


class Recipient(db.Model):
    """
    A recipient is the person or entity who receives some meals.
    Usually, a recipient is also involved in paying for and making said recipes, but not necessarily.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(16), nullable=True)
    email = db.Column(db.String(128), nullable=True)


class RecipientSessionRecipe(db.Model):
    """
    This describes which recipes are made in a session, how many, and who they go to.
    meal_count describes how many instances of a recipe a recipient is signed up for,
    e.g. the number of times they want to make that recipe.
    I'm not sure that I want to let user sign up for partial meals,
    but this schema will allow that since meal_count is a Float.
    """
    recipient_id = db.Column(db.Integer(), db.ForeignKey('recipient.id'), primary_key=True)
    session_id = db.Column(db.Integer(), db.ForeignKey('session.id'), primary_key=True)
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'), primary_key=True)
    meal_count = db.Column(db.Float(), nullable=False)

    recipient = db.relationship('Recipient')
    session = db.relationship('Session')
    recipe = db.relationship('Recipe')

    @property
    def cost(self) -> float:
        """The cost of this number of meals"""
        return self.recipe.cost * self.meal_count
