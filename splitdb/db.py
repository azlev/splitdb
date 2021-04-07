from django.db.models.fields.related import ForeignKey, ManyToManyField


class DBRouter:

    other_databases = { 'integration' }

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.other_databases:
            return app_label
        return None

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.other_databases:
            return app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, **hints):
        if db in self.other_databases:
            return db == app_label
        if db == "default" and app_label in self.other_databases:
            return False
        return True


class SpanningForeignKey(ForeignKey):
    """
    Class initially created by Jared Scott available on
    https://gist.github.com/gcko/de1383080e9f8fb7d208.
    This class will overwrite validate and __init__ to allow a model ForeignKey be created
    but without database FOREIGN KEY constraint. There are no constraint between databases.

    At Django 3 the method validate will have to be update if it isn't compatible with
    multiple databases.
    """

    def __init__(self, to, on_delete, related_name=None, related_query_name=None,
                 limit_choices_to=None, parent_link=False, to_field=None, **kwargs):
        """
        Method overwritten to always use db_constraint as False.
        This field should be used to make relation between databases and for that there is no
        constraint.
        :param to: (django.models.Model) Class model to Foreign Key.
        :param on_delete: (integer) Constant to specified action on delete
        :param related_name: (str) Related name to use on reverse object lookup.
        :param related_query_name: (str) Related name to use on reverse query lookup.
        :param limit_choices_to: (List) List of filters to restrict queryset to.
        :param parent_link: (boolean) Specifies whether to treat Foreign Field as link to
        parent model class or not.
        :param to_field: (str) Field name use on Backward compatibility for ManyToOneRel.
        :param db_constraint: (boolean) whether to have constraint at database level or not.
        :param kwargs: (dict) Additional key arguments to pass.
        """
        # We make sure that db_constraint is always False
        db_constraint = False

        if 'db_constraint' in kwargs:
            del kwargs['db_constraint']

        super(SpanningForeignKey, self).__init__(
            to=to,
            on_delete=on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs
        )


class SpanningManyToManyField(ManyToManyField):
    """
    Class created to allow identification of ManyToManyField between database.
    """

    def __init__(self, to, related_name=None, related_query_name=None,
                 limit_choices_to=None, symmetrical=None, through=None,
                 through_fields=None, db_table=None,
                 swappable=True, **kwargs):
        """
        Method overwritten to always make use of db_constraint as False.
        This field should be used to make relation between databases and for that there is no
        constraint.
        :param to: (django.models.Model) Class model to Foreign Key.
        :param related_name: (str) Related name to use on reverse object lookup.
        :param related_query_name: (str) Related name to use on reverse query lookup.
        :param limit_choices_to: (List) List of filters to restrict queryset to.
        :param symmetrical: (boolean) Whether relationship between models should be symmetrical.
        :param through: (django.models.Model) Class model to intermediary model.
        :param through_fields: (List) List of fields that should be used in relationship to avoid
        conflict when a through model has more than one ForeignKey to same model.
        :param db_constraint: (boolean) whether to have constraint at database level or not.
        :param db_table: (str) Table name for the attributive-associative table.
        :param swappable: (boolean) Whether the relationship make use o swappable models, e.g.
        settings.AUTH_USER_MODEL.
        :param kwargs: (dict) Additional key arguments to pass.
        """
        db_constraint = False

        if 'db_constraint' in kwargs:
            del kwargs['db_constraint']

        super(SpanningManyToManyField, self).__init__(
            to=to,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            symmetrical=symmetrical,
            through=through,
            through_fields=through_fields,
            db_constraint=db_constraint,
            db_table=db_table,
            swappable=swappable,
            **kwargs
        )
