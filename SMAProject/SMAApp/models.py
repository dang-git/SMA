from django.db import models
from mongoengine import *
import datetime
# Create your models here.

connect('smadb')

class Snapshot(Document):
    _id = ObjectIdField()
    keyword = StringField(max_length=60)
    owner = ReferenceField('User')
    platform = StringField()
    # platform = ReferenceField('Ref_platform')
    snapshot_name = StringField()
    extracted_data = ListField()
    date_extracted = DateTimeField()
    chart_data = ListField(ReferenceField('Chart')) # TODO there should be many charts in 1 snapshot
    insights = ListField()
    wordcloud_image = ImageField()
    date_created = DateTimeField(default=datetime.datetime.utcnow)

class User(Document):
    user_id = ObjectIdField()
    email = StringField() # this will be required
    password = StringField()
    snapshots = ListField(ReferenceField('Snapshot'))

class Client(Document):
    client_name = StringField()
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




