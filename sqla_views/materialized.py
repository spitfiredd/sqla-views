from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
from sqlalchemy import MetaData, Table, event, Column, DDL


class CreateMaterializedView(DDLElement):
    """Create materialized view, for postresql
    https://www.postgresql.org/docs/11/sql-creatematerializedview.html
    """
    def __init__(self, name, selectable, if_exists=False):
        self.name = name
        self.selectable = selectable
        self.if_exists = if_exists


@compiler.compiles(CreateMaterializedView)
def compile_create_materialized_view(element, compiler, **kwargs):
    ddl = "CREATE MATERIALIZED VIEW "
    if element.if_exists:
        ddl += "IF NOT EXISTS "
    ddl += f"{element.name} "
    ddl += f"AS {compiler.sql_compiler.process(element.selectable,literal_binds=True)}"
    return ddl


class DropMaterializedView(DDLElement):
    """Drop Materialzed view, postgresql,
    https://www.postgresql.org/docs/11/sql-dropmaterializedview.html
    """
    def __init__(self, name, if_exists=True, cascade=True):
        self.name = name
        self.if_exists = if_exists
        self.cascade = cascade


@compiler.compiles(DropMaterializedView)
def compile_drop_materialized_view(element, compiler, **kwargs):
    ddl = "DROP MATERIALIZED VIEW "
    if element.if_exists:
        ddl += "IF EXISTS "
    ddl += f"{element.name} "
    if element.cascade:
        ddl += "CASCADE"
    return ddl


class RefreshMaterializedView(DDLElement):
    """Refresh Materialized view, postresql,
    https://www.postgresql.org/docs/11/sql-refreshmaterializedview.html

    """
    def __init__(self, name, concurrently=False):
        self.name = name
        self.concurrently = concurrently


@compiler.compiles(RefreshMaterializedView)
def compile_refresh_materialed_view(element, compiler, **kwargs):
    ddl = "REFRESH MATERIALIZED VIEW "
    if element.concurrently:
        ddl += "CONCURRENTLY "
    ddl += f"{element.name}"
    return ddl


def create_materialized_view(name, selectable, metadata=MetaData()):
    t = Table(name, metadata)
    for c in selectable.c:
        t.append_column(Column(c.name, c.type, primary_key=c.primary_key))

    event.listen(
        metadata,
        'after_create',
        CreateMaterializedView(name, selectable)
    )

    event.listen(
        metadata,
        'before_drop',
        DDL('DROP MATERIALIZED VEIW IF EXISTS '.format(name))
    )
    return t
