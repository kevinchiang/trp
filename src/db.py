import os
import sqlalchemy

DB_DRIVER = os.environ['DB_DRIVER']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_SCHEMA = os.environ['DB_SCHEMA']

if DB_DRIVER == 'sqlite':
    connection_string = f"{DB_DRIVER}://{DB_HOST}"
else:
    connection_string = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
engine = sqlalchemy.create_engine(connection_string)

