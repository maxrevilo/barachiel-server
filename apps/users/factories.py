import random
import factory
from faker import Factory
from apps.users.models import User

fake = Factory.create()

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        strategy = factory.BUILD_STRATEGY

    name =  factory.LazyAttribute(lambda o: fake.name())
    email = factory.Sequence(lambda n: 'user%d@u.com' % n)
    password = "pbkdf2_sha256$12000$657ISm2WR31E$MCA9nMWbcmRHOtxmxQaoiVLTQsrmeZbZfWXv2KFLuMk="
    picture = None

class UserInRadius(UserFactory):
    _geo_here = {
       'lat': 51.5033630,
       'lon': -0.1276250
    }
    geo_lat =  factory.LazyAttribute(lambda o: float(fake.geo_coordinate(_geo_here['lat'], 0.001)))
    geo_lon =  factory.LazyAttribute(lambda o: float(fake.geo_coordinate(_geo_here['lon'], 0.001)))

class FullUserFactory(UserFactory):
    tel =  factory.LazyAttribute(lambda o: fake.phone_number())
    sex =  factory.LazyAttribute(lambda o: random.choice(['F','M'])) 
    r_interest =  factory.LazyAttribute(lambda o: random.choice(['F','M','B','R'])) 
    bio =  factory.LazyAttribute(lambda o: fake.sentences())
    birthday =  factory.LazyAttribute(lambda o: fake.date_time_between("-60y", "-10y").date())
    sentimental_status =  factory.LazyAttribute(lambda o: random.choice(['S','M','R'])) 
    geo_lat =  factory.LazyAttribute(lambda o: float(fake.latitude()))
    geo_lon =  factory.LazyAttribute(lambda o: float(fake.latitude()))

class FullUserInRadiusFactory(FullUserFactory):
    _geo_here = {
       'lat': 51.5033630,
       'lon': -0.1276250
    }
    geo_lat =  factory.LazyAttribute(lambda o: float(fake.geo_coordinate(_geo_here['lat'], 0.001)))
    geo_lon =  factory.LazyAttribute(lambda o: float(fake.geo_coordinate(_geo_here['lon'], 0.001)))

