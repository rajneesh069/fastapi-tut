from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///mydb.db", echo=True)

conn = engine.connect()

conn.execute(text("CREATE TABLE IF NOT EXISTS users(name str, age int);"))

conn.commit()

from sqlalchemy.orm import Session

session = Session(engine)

session.execute(text('INSERT INTO users (name, age) VALUES("Rajneesh", "22")'))

session.commit()
