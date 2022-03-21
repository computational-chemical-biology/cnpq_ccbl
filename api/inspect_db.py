#https://towardsdatascience.com/sql-and-etl-an-introduction-to-sqlalchemy-in-python-fc66e8be1cd4
import sqlalchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import sqlalchemy as db

engine = db.create_engine('sqlite:///tree_of_life.db')
metadata = MetaData()
metadata.create_all(engine)
inspector = inspect(engine)
inspector.get_columns('tree_of_life')
with engine.connect() as con:
    rs = con.execute('SELECT * FROM tree_of_life')
    rows = []
    for row in rs:
        rows.append(row)


with engine.connect() as con:
    rs = con.execute("""SELECT COUNT(id)
                     FROM tree_of_life;""")
    for row in rs:
        print(row)
