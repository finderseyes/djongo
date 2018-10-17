from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from logging import getLogger

logger = getLogger(__name__)


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    sql_create_index = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s INDEX (%(columns)s)%(extra)s"
    sql_delete_index = "DROP INDEX %(table)s (%(name)s)"

    def _constraint_names(self, model, column_names=None, unique=None,
                          primary_key=None, index=None, foreign_key=None,
                          check=None, type_=None):
        if column_names is not None:
            column_names = [
                self.connection.introspection.column_name_converter(name)
                for name in column_names
            ]
        with self.connection.cursor() as cursor:
            constraints = self.connection.introspection.get_constraints(cursor, model._meta.db_table)

        result = []
        for name, infodict in constraints.items():
            if column_names is None or column_names == infodict['columns']:
                if unique is not None and infodict['unique'] != unique:
                    continue
                if primary_key is not None and infodict['primary_key'] != primary_key:
                    continue
                if index is not None and infodict['index'] != index:
                    continue
                if check is not None and infodict['check'] != check:
                    continue
                if foreign_key is not None and not infodict['foreign_key']:
                    continue

                result.append(name)
        return result

