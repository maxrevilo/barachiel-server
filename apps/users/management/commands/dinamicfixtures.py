from django.core.management.base import BaseCommand, CommandError
from django_dynamic_fixture import G
from faker import Factory
#from django.contrib.auth.hashers import make_password
from apps.users.models import User
from apps.likes.models import Like

class Command(BaseCommand):
    help = 'adds dinamic fixtures to the database'

    def handle(self, *args, **options):
        ### INIT ###
        fake = Factory.create()
        password = "pbkdf2_sha256$12000$657ISm2WR31E$MCA9nMWbcmRHOtxmxQaoiVLTQsrmeZbZfWXv2KFLuMk="

        ### LOGIN TESTS ###
        if User.objects.filter(email='test1@t.com').exists():
            User.objects.filter(email='test1@t.com').delete()
        G(User, name=fake.name(), email='test1@t.com', password=password, picture=None)
        print('Test user Generated...')
