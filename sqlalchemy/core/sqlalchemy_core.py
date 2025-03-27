# When you work with SQLAlchemy Core then you work with the Metadata object, and when you work with SQLAlchemy ORM, you work with mapped classes (often defined using the declarative base).
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    UUID,
    String,
    Float,
    ForeignKey,
    func,
)
from uuid import uuid4
import random

# engine = create_engine("sqlite:///mydb.db", echo=True) :  Prints the SQL commands which run and shows DB logs
engine = create_engine("sqlite:///mydb.db", echo=False)
meta = MetaData()

users = Table(
    "users",
    meta,
    Column("id", UUID, primary_key=True, default=lambda: uuid4()),
    Column("name", String, nullable=False),
    Column("age", Integer),
)

things = Table(
    "things",
    meta,
    Column("id", UUID, primary_key=True, default=lambda: uuid4()),
    Column("name", String, nullable=False),
    Column("price", Float, nullable=False),
    Column("owner", UUID, ForeignKey("users.id")),
)

meta.create_all(engine)  # create table if not exists

# connection object is needed to work with these tables
conn = engine.connect()

insert_statement = users.insert().values(id=uuid4(), name="Rajneesh", age=22)
result = conn.execute(insert_statement)
conn.commit()

select_statement = users.select().where(users.c.name == "Rajneesh")
result = conn.execute(select_statement)
for row in result.fetchall():
    print(row)

update_statement = (
    users.update().where(users.c.name == "Rajneesh").values(name="Sachin")
)
conn.execute(update_statement)
conn.commit()

delete_statement = users.delete().where(users.c.age == 22)
result = conn.execute(delete_statement)
conn.commit()


users_insert_statement = users.insert().values(
    [
        {"name": "Alice", "age": 28},
        {"name": "Bob", "age": 34},
        {"name": "Charlie", "age": 22},
        {"name": "Diana", "age": 27},
        {"name": "Ethan", "age": 30},
    ]
)


things_insert_statement = things.insert().values(
    [
        {"name": "Laptop", "price": 1299.99},
        {"name": "Smartphone", "price": 699.50},
        {"name": "Headphones", "price": 199.99},
        {"name": "Monitor", "price": 299.99},
        {"name": "Keyboard", "price": 89.99},
        {"name": "Mouse", "price": 49.99},
        {"name": "Printer", "price": 149.99},
        {"name": "Tablet", "price": 399.99},
        {"name": "External Hard Drive", "price": 99.99},
        {"name": "Webcam", "price": 59.99},
    ]
)

conn.execute(users_insert_statement)
conn.commit()  # commit after each statement for the db to have that data
conn.execute(things_insert_statement)
conn.commit()

# select statement to show all the data from users table
users_select_statement = users.select()
result = conn.execute(users_select_statement)
print("Users Table Data:")
for row in result.fetchall():
    print(row)

# select statement to show all the data from things table
things_select_statement = things.select()
result = conn.execute(things_select_statement)
print("Things Table Data:")
for row in result.fetchall():
    print(row)


# updating the things table with random user IDs

# select statement for all users' ids
get_all_user_ids_select_statement = users.select()
result = conn.execute(get_all_user_ids_select_statement)
all_user_ids = [row[0] for row in result.fetchall()]

# select statement for all things' ids
get_all_things_ids_select_statement = things.select()
result = conn.execute(get_all_things_ids_select_statement)
all_things_ids = [row[0] for row in result.fetchall()]

# update statement to give user ids to each thing
things_table_update_statement = (
    things.update()
    .where(things.c.owner == None)
    .values(owner=random.choice(all_user_ids))
)
result = conn.execute(things_table_update_statement)
conn.commit()


# select statement to show all the data from users table
users_select_statement = users.select()
result = conn.execute(users_select_statement)
print("Users Table Data:")
for row in result.fetchall():
    print(row)

# select statement to show all the data from things table
things_select_statement = things.select()
result = conn.execute(things_select_statement)
print("Things Table Data:")
for row in result.fetchall():
    print(row)


"""
Sample Output: 
(.venv) rajne@rajneesh69:/d/python/fastapi-tut/sqlalchemy/core$ python sqlalchemy_core.py
Users Table Data:
(UUID('bf1a7953-750f-48aa-af3d-a4064fc810d7'), 'Alice', 28)
(UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'), 'Bob', 34)
(UUID('4c910150-b7f4-4e20-bb2c-57fa55930246'), 'Charlie', 22)
(UUID('b7c349b7-8104-4e76-a69b-83e911139453'), 'Diana', 27)
(UUID('29fe741a-4acf-4e71-b07b-20323eae3654'), 'Ethan', 30)
Things Table Data:
(UUID('902167c1-34b3-4dd4-85f6-585f3b2a82c1'), 'Laptop', 1299.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('6fac3fb5-8a0f-42f4-b0e0-fc60824ae7e6'), 'Smartphone', 699.5, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('a98d121b-e7c4-4375-8bbf-abebcd540f1f'), 'Headphones', 199.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('7b3f199d-6f59-4c9a-ad07-5d407b4a2d9b'), 'Monitor', 299.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('92dcf8db-f914-4e64-b331-6b3ef06efa52'), 'Keyboard', 89.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('7818434d-7b9e-4bcf-a786-d1efc786cf98'), 'Mouse', 49.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('003c961c-9723-41a9-99c8-ce1e03aeb8f0'), 'Printer', 149.99, UUID('b7c349b7-8104-4e76-a69b-83e911139453'))
(UUID('9e502b53-355a-4168-a5b3-931bb534186b'), 'Tablet', 399.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('fbb2e356-2753-4732-962c-f523a304dff2'), 'External Hard Drive', 99.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
(UUID('26a060d2-8018-4989-b377-83e5c2e3e15d'), 'Webcam', 59.99, UUID('e3d9e4c3-d98c-4981-8dbf-c69eba584389'))
"""


# join statement
join_statement = users.join(
    things, things.c.owner == users.c.id
)  # inner join by default
join_statement = users.outerjoin(
    things, things.c.owner == users.c.id
)  # basically a left join
# full outer joins aren't supported out of the box
select_statement = (
    users.select()
    .with_only_columns(users.c.name, things.c.name)
    .select_from(join_statement)
)
result = conn.execute(select_statement)
for row in result.fetchall():
    print(row)


group_by_stmt = (
    things.select()
    .with_only_columns(things.c.owner, func.sum(things.c.price))
    .group_by(things.c.owner)
)
result = conn.execute(group_by_stmt)
for row in result.fetchall():
    print(row)
