from sqlalchemy.sql import text
from sqla_views.materialized import CreateMaterializedView, DropMaterializedView


def test_create_view_query_strings():
    query = text("SELECT * FROM my_table")
    view = CreateMaterializedView('my_view', query)
    view_string = str(view.compile())
    test_string = 'CREATE MATERIALIZED VIEW my_view AS SELECT * FROM my_table'
    assert view_string == test_string
