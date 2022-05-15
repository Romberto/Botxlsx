import datetime as datetime
import peewee
from peewee import SqliteDatabase, CharField, Model, IntegerField, FloatField, ForeignKeyField
from loader import dp

db = SqliteDatabase('data/database.db')


# r'/root/StructurBot/data/database.db'

class Report(Model):
    year = IntegerField()
    month = IntegerField()
    manufacturer = CharField(null=True)
    departure_region = CharField(null=True)
    departure_station = CharField(null=True)
    product = CharField(null=True)
    volume = FloatField(null=True)
    swagons = IntegerField(null=True)
    fraction = CharField(null=True)
    breed = CharField(null=True)
    durance = IntegerField(null=True)
    customer = CharField(null=True)
    customer_stantion = CharField(null=True)
    customer_region = CharField(null=True)

    class Meta:
        database = db


class Users(Model):
    chat_id = IntegerField()
    first_name = CharField(null=True)
    last_name = CharField(null=True)

    class Meta:
        database = db


class LookingReport(Model):
    user = ForeignKeyField(Users)
    datetime = peewee.DateTimeField(default=datetime.datetime.now)
    description = CharField()

    class Meta:
        database = db

