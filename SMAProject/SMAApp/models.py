from django.db import models
from mongoengine import DynamicDocument,Document, BinaryField, DictField, ObjectIdField, StringField, IntField, ListField, DateTimeField, FileField, ImageField, ReferenceField, FloatField, EmbeddedDocument, EmbeddedDocumentField
import datetime
# Create your models here.

# connect('smadb')

class Snapshot(DynamicDocument):
    _id = ObjectIdField()
    keyword = StringField(max_length=60)
    platform = StringField()
    # platform = ReferenceField('Ref_platform')
    snapshot_name = StringField()
    extracted_data = ListField()
    quick_stats = DictField()
    influencers_data = DictField()
    influential_data = DictField()
    date_extracted = DateTimeField()
    chart_data = ListField()
    lda_data = DictField()
    wordcloud_image = ImageField() # wordcloud_image = FileField()
    insights = ListField()
    owner = ObjectIdField() # ReferenceField('User')
    date_created = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'db_alias': 'default'}

class User(Document):
    _id = ObjectIdField()
    username = StringField()
    email = StringField() # this will be required
    password = StringField()
    address = StringField()
    snapshots = ListField() #ListField(ReferenceField('Snapshot'))
    license_type = StringField()
    ## USERNAME_FIELD = 'email'
    ## REQUIRED_FIELDS = ['username','address','license_type']
    
    meta = {'db_alias': 'default'}

#UNUSED
class WordCloudImageMask(Document):
    image = ImageField()
    owner = StringField()
    uploaded_at = DateTimeField(default=datetime.datetime.utcnow)

#UNUSED
class Organization(Document):
    org_name = StringField()
    address = StringField()
    users = ListField(ReferenceField('User'))
    license_type = StringField()

# Chart Related

#UNUSED
class Chart(Document):
    # chart_id = ObjectId()
    chart_container = StringField()
    chart_data = DictField()

#UNUSED
class Chart_point(Document):
    chart_point_id = ObjectIdField()


""" SMA Words """

class Idioms(Document):
    word = StringField(unique=True)
    measure = FloatField()
    # idiom_list = ListField()
    owner =  StringField() #Set to ObjectIdField() or ReferenceField(User) in the future
    # word = StringField()
    # measure = FloatField()

    meta = {'db_alias': 'smawords'}

    # @queryset_manager
    # def check_if_idiom_owner_exists(doc_cls,queryset,):
    #     return queryset.filter(idiomowner)

class Boosters(Document):
    word = StringField(unique=True)
    measure = FloatField()
    owner = StringField() #Set to ObjectIdField() or ReferenceField(User) in the future
    # word = StringField()
    # measure = FloatField()
    meta = {'db_alias': 'smawords'}


# class Names(Document):
#     name_list = ListField()
#     name_owner = StringField()
#     # idioms = ListField(EmbeddedDocumentField(Idioms))
#     meta = {'db_alias': 'smawords'}

class Names(Document):
    name = StringField(unique=True)
    owner = StringField()
    meta = {'db_alias': 'smawords'}

class Lexicons(Document):
    word = StringField(unique=True)
    measure = FloatField()
    owner = StringField()
    meta = {'db_alias': 'smawords'}

# class BaseFormWord(EmbeddedDocument):
#     word = StringField(unique=True)
#     baseform = StringField()
#     meta = {'db_alias': 'smawords'}
    
class BaseForms(Document):
    word = StringField(unique=True)
    baseform = StringField()
    #baseform_list = ListField() #ListField(EmbeddedDocumentField(BaseFormWord))
    owner = StringField()
    meta = {'db_alias': 'smawords'}

# class Negate(Document):
#     negate_list = ListField()
#     negate_owner = StringField()
#     meta = {'db_alias': 'smawords'}

class Negate(Document):
    word = StringField(unique=True)
    owner = StringField()
    meta = {'db_alias': 'smawords'}

class Emojis(Document):
    # emoji_list = ListField()
    word = StringField(unique=True)
    measure = StringField(unique=True)
    owner = StringField()
    meta = {'db_alias': 'smawords'}



