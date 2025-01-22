class DatabaseRouter:
    """
    A router to control all database operations on models in the
    users_app, products_app, and orders_app applications.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users_app':
            return 'users_db'
        elif model._meta.app_label == 'products_app':
            return 'products_db'
        elif model._meta.app_label == 'orders_app':
            return 'orders_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users_app':
            return 'users_db'
        elif model._meta.app_label == 'products_app':
            return 'products_db'
        elif model._meta.app_label == 'orders_app':
            return 'orders_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'users_app':
            return db == 'users_db'
        elif app_label == 'products_app':
            return db == 'products_db'
        elif app_label == 'orders_app':
            return db == 'orders_db'
        return None

