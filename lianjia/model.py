# -*- coding: utf-8 -*-

from peewee import *

db = MySQLDatabase('lianjia', host='localhost', port=3306, user='root', passwd='12345678',
                   charset='utf8')


# define base model
class BaseModel(Model):
    class Meta:
        database = db

class LianjiaInfo(BaseModel):
    region = CharField()
    community = CharField()
    deal_time = CharField()
    total_price = CharField()
    unit_price = CharField()
    style = CharField()
    floor = CharField()
    size = CharField()
    orientation = CharField()
    build_year = CharField()
    decoration = CharField()
    property_time = CharField()
    elevator = CharField()
    info = TextField()

db.connect()
db.create_tables([LianjiaInfo], safe=True)
