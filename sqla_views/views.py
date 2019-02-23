from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table
from sqlalchemy.ext import compiler


class CreateView(DDLElement):
    def __init__(self, name, selectable, replace=True):
        self.name = name
        self.selectable = selectable
        self.replace = replace


@compiler.compiles(CreateView)
def complile_create_view(element, compiler, **kwargs):
    ddl = "CREATE "
    if element.replace:
        ddl += "OR REPLACE "
    ddl += f"VIEW {element.name} "
    ddl += f"AS {compiler.sql_compiler.process(element.selectable,literal_binds=True)}"
    return ddl


class DropView(DDLElement):
    def __init__(self, name, if_exists=True, cascade=True):
        self.name = name
        self.if_exists = if_exists
        self.cascade = cascade


@compiler.compiles(DropView)
def compile_drop_view(element, compiler, **kwargs):
    ddl = "DROP VIEW "
    if element.if_exists:
        ddl += "IF EXISTS "
    ddl += f"{element.name}"
    if element.cascade:
        ddl += " CASCADE"
    return ddl


def create_view(name, metadata, selectable):
    t = table(name)

    for c in selectable.c:
        c._make_proxy(t)

    CreateView(name, selectable).execute_at('after-create', metadata)
    DropView(name).execute_at('before-drop', metadata)
    return t
