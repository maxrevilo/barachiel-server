from django.core.management.base import BaseCommand, CommandError
from apps.users.models import User
from apps.likes.models import Like
from apps.users.factories import UserFactory, FullUserInRadiusFactory

class Command(BaseCommand):
    help = 'adds dinamic fixtures to the database'

    def handle(self, *args, **options):

        ### LOGIN TESTS ###
        if User.objects.filter(email='authtest@t.com').exists():
            User.objects.filter(email='authtest@t.com').delete()
        UserFactory.create(email='authtest@t.com')
        print('Login user Generated...')

        ### WAVE TESTS ###
        #geo_here = {
           #'lat': 51.5033630,
           #'lon': -0.1276250
        #}
        #geo_far = {
            #'lat': 10.1579310,
            #'lon': -67.9972100
        #}
        #for i in range(1, 10):
            #if User.objects.filter(email='wavetest%d@t.com' % i).exists():
                #User.objects.filter(email='wavetest%d@t.com' % i).delete()
            #geoloc = geo_here if i < 6 else geo_far
            #G(
                #User, 
                #name=fake.name(), 
                #email='wavetest%d@t.com' % i, 
                #password=password, 
                #picture=None, 
                #geo_lat=geoloc['lat'], 
                #geo_lon=geoloc['lon']
            #)
        #print('Wave users Generated...')

        ### WAVE BACK TESTS ###
