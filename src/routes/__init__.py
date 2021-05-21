from src.routes import aisle, ingredient, recipe, session, signup

__all__ = [aisle, ingredient, recipe, session, signup]

blueprints = [module.blueprint for module in __all__]
