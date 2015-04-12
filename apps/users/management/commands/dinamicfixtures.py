from django.core.management.base import BaseCommand, CommandError
from apps.users.models import User
from apps.likes.models import Like
from apps.users.factories import UserFactory, FullUserFactory, FullUserInRadiusFactory

class Command(BaseCommand):
    help = 'adds dinamic fixtures to the database'

    def handle(self, *args, **options):

        ### LOGIN TESTS ###
        if User.objects.filter(email='authtest@t.com').exists():
            User.objects.filter(email='authtest@t.com').delete()
        UserFactory.create(email='authtest@t.com')
        print('Login user Generated...')

        ### WAVE TESTS ###
        geo_here = {
           'lat': 51.5033630,
           'lon': -0.1276250
        }
        geo_far = {
            'lat': 10.1579310,
            'lon': -67.9972100
        }
        for i in range(1, 10):
            if User.objects.filter(email='wavetest@t.com').exists():
                User.objects.filter(email='wavetest@t.com').delete()
            FullUserFactory.create(
                email='wavetest@t.com',
                geo_lat=geo_here['lat'], 
                geo_lon=geo_here['lon']
            )

            if User.objects.filter(email='wavetest%d@t.com' % i).exists():
                User.objects.filter(email='wavetest%d@t.com' % i).delete()
            if i < 6:
                FullUserInRadiusFactory.create(email='wavetest%d@t.com' % i)
            else:
                FullUserInRadiusFactory.create(
                    email='wavetest%d@t.com' % i,
                    geo_lat=geo_far['lat'], 
                    geo_lon=geo_far['lon']
                )
        print('Wave users Generated...')

        ### WAVE BACK TESTS ###
