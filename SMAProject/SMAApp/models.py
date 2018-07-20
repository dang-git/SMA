from django.db import models
from mongoengine import *
import datetime
# Create your models here.

connect('smadb')

class Snapshot(DynamicDocument):
    _id = ObjectIdField()
    keyword = StringField(max_length=60)
    platform = StringField()
    # platform = ReferenceField('Ref_platform')
    snapshot_name = StringField()
    extracted_data = ListField()
    date_extracted = DateTimeField()
    chart_data = ListField() # TODO there should be many charts in 1 snapshot
    lda_data = DictField()
    insights = ListField()
    wordcloud_image = ImageField()
    owner = StringField() #ReferenceField('User')
    date_created = DateTimeField(default=datetime.datetime.utcnow)

class User(Document):
    _id = ObjectIdField()
    username = StringField()
    email = StringField() # this will be required
    password = StringField()
    address = StringField()
    snapshots = ListField() #ListField(ReferenceField('Snapshot'))
    license_type = StringField()


class Organization(Document):
    org_name = StringField()
    address = StringField()
    users = ListField(ReferenceField('User'))
    license_type = StringField()

# Chart Related

class Chart(Document):
    # chart_id = ObjectId()
    chart_container = StringField()
    chart_data = DictField()

class Chart_point(Document):
    chart_point_id = ObjectIdField()

    




