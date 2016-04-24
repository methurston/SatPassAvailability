from peewee import *


db = SqliteDatabase('peewee.db')


class BaseModel(Model):
    class Meta:
        database = db


class Satellite(BaseModel):
    name = CharField(primary_key=True)
    lineone = CharField()
    linetwo = CharField()
    updateDTS = DateField()


class Location(BaseModel):
    callsign = CharField(primary_key=True)
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
if len(db.get_tables()) == 0:
    print 'Schema not found: creating'
    all_tables = [Satellite, Location, Timeslot, SatelliteInfo]
    db.create_tables(all_tables)
