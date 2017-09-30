class TwistreapyDatabaseRouter(object):
    def db_for_read(self, model, **hints):
        """Send all read operations on twistreapy app models to `rest`."""
        if model._meta.app_label == 'twistreapy':
            return 'twistreapy'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on twistreapy app models to `rest`."""
        if model._meta.app_label == 'twistreapy':
            return 'twistreapy'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        # Allow any relation between two models that are both in the twistreapy app.
        if obj1._meta.app_label == 'twistreapy' and obj2._meta.app_label == 'twistreapy':
            return True
        # No opinion if neither object is in the twistreapy app (defer to default or other routers).
        elif 'twistreapy' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the twistreapy app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the twistreapy app's models get created on the right database."""
        if app_label == 'twistreapy':
            # The twistreapy app should be migrated only on the rest database.
            return db == 'twistreapy'
        elif db == 'twistreapy':
            # Ensure that all other apps don't get migrated on the rest database.
            return False

        # No opinion for all other scenarios
        return None