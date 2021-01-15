from peewee import SqliteDatabase
from pkg_resources import resource_filename


db = SqliteDatabase(resource_filename(__name__, 'data.db'))
db.connect()
