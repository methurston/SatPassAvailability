from peewee import *


db = SqliteDatabase('peewee.db')


class BaseModel(Model):
    class Meta:
        database = db

class Satellite(BaseModel):
    name = CharField()
    lineone = CharField()
    linetwo = CharField()
    updateDTS = DateField()


class Location(BaseModel):
    callsign = CharField()
    lat = FloatField()
    lon = FloatField()
    elevation = IntegerField()
    timezone = CharField()


class Timeslot(BaseModel):
    callsign = ForeignKeyField(Location, related_name='loc_callsign')
    weekdays = CharField()
    start_time = CharField()
    duration = IntegerField()


class SatelliteInfo(BaseModel):
    name = ForeignKeyField(Satellite, related_name='sat_name')
    uplink = FloatField()
    downlink = FloatField()
    modes = CharField


db.connect()
db.create_tables([Satellite, Location, Timeslot, SatelliteInfo])
