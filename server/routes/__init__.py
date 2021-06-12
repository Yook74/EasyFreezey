from server.routes import aisle, ingredient, recipe, session, signup, recipient

__all__ = [aisle, ingredient, recipe, session, signup, recipient]

blueprints = [module.blueprint for module in __all__]
