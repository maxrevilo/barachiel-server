# -*- coding: utf-8 -*-

import json
from datetime import date, datetime, timedelta

#from django.contrib.auth.tokens import default_token_generator
#from django.utils.http import int_to_base36
#from django.template import Context, loader
#from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.views.generic import View
from django.shortcuts import get_object_or_404
#from django.contrib.auth.decorators import login_required

from libs.helpers import PUT, change_in_latitude, change_in_longitude, haversine_distance
from libs.decorators import is_authenticated_or_401
from models import User
from apps.auth.signals import user_with_new_email


class UsersInstanceView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        user_id = kwargs['id']
        if user_id == 'me':
            user = request.user
        else:
            user = get_object_or_404(User, id=user_id)

        response = user.serialize(request.user)

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    @is_authenticated_or_401
    def put(self, request, *args, **kwargs):
        user = request.user
        resp = {'settings': {}}
        #TODO Chequear y limpiar entradas

        name = PUT(request, 'name')
        if name:
            user.name = name
            resp['name'] = name

        # email = PUT(request, 'email_wtc')
        # if email:
        #     user.email = email
        #     resp['email'] = email

        send_user_with_new_email = False
        email_wtc = PUT(request, 'email_wtc')
        if email_wtc and email_wtc != user.email:
            from django.db.models import Q
            users_using_this_email = User.objects.filter(Q(email=email_wtc) | Q(_email_wtc=email_wtc))
            if len(users_using_this_email) > 0:
                return HttpResponseForbidden("Email address is already being used")
            user._email_wtc = email_wtc
            resp['email_wtc'] = email_wtc
            send_user_with_new_email = True

        tel = PUT(request, 'tel')
        if tel:
            user.tel = tel
            resp['tel'] = tel

        r_interest = PUT(request, 'r_interest')
        if r_interest:
            user.r_interest = r_interest
            resp['r_interest'] = r_interest

        sentimental_status = PUT(request, 'sentimental_status')
        if sentimental_status:
            user.sentimental_status = sentimental_status
            resp['sentimental_status'] = sentimental_status

        sex = PUT(request, 'sex')
        if sex:
            user.sex = sex
            resp['sex'] = sex

        birthday = PUT(request, 'birthday')
        if birthday:
            user.birthday = date.fromordinal(datetime.strptime(birthday, '%Y-%m-%d').toordinal())
            resp['birthday'] = user.birthday.isoformat() if user.birthday is not None else None

        age = PUT(request, 'age')
        if age:
            user.age = age
            resp['age'] = age

        bio = PUT(request, 'bio')
        if bio:
            user.bio = bio
            resp['bio'] = bio

        password = PUT(request, 'password')
        if password:
            newpassword = PUT(request, 'new_password')
            if newpassword:
                if (user.check_password(password)):
                    user.set_password(newpassword)
                else:
                    return HttpResponseForbidden()

        #Position:
        geo_lat = PUT(request, 'geo_lat')
        geo_lon = PUT(request, 'geo_lon')
        if geo_lat and geo_lon:
            geo_lat = json.loads(geo_lat)
            geo_lon = json.loads(geo_lon)
            user.geo_lat = geo_lat
            user.geo_lon = geo_lon
            user.geo_time = datetime.now()

        #Settings:
        off_radar = PUT(request, 'off_radar')
        if off_radar:
            user.off_radar = (off_radar == 'true')
            resp['settings']['off_radar'] = user.off_radar

        user.save()
        if send_user_with_new_email:
            user_with_new_email.send(sender=self, user=user, user_just_created=False)
        return HttpResponse(json.dumps(resp), mimetype='application/json')

    @is_authenticated_or_401
    def delete(self, request, *args, **kwargs):

        user = request.user
        user.delete()
        return HttpResponse()


class UsersListView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.geo_time < datetime.now() - settings.TIME_TO_GHOSTING:
            return HttpResponse(status=203)

        limit = 20
        if request.GET.__contains__('l'):
            limit = min(int(request.GET['l']), 100)

        query = ''
        if request.GET.__contains__('q'):
            query = request.GET.get('q')

        ulat = user.geo_lat
        ulon = user.geo_lon

        if ulat == 0 and ulon == 0:
            response = []
        else:
            dlat = change_in_latitude(settings.RADAR_RAIUS)
            dlon = change_in_longitude(ulat, settings.RADAR_RAIUS)

            #print "lat [%f, %f] lon [%f, %f]" % (ulat-dlat, ulat+dlat, ulon-dlon, ulon+dlon)

            users = User.objects.filter(
                            # Filter by time
                            geo_time__gt=datetime.now() - settings.TIME_TO_GHOSTING,
                            # Filter by distance
                            geo_lat__gte=ulat-dlat,
                            geo_lat__lte=ulat+dlat,
                            geo_lon__gte=ulon-dlon,
                            geo_lon__lte=ulon+dlon,
                        ).exclude(
                            id__exact=user.id
                        )\
                        .filter(name__icontains=query)[:limit]

            #response = map(lambda u: u.preview(request.user), users) #TODO: DESCOMENTAR

            #TODO optimizar para producción y filtrar los más lejanos.
            user_pos = (ulat, ulon)
            response = []
            for u in users:
                r = u.preview(request.user)
                if settings.IGNORE_DISTANCE:
                    r['d'] = 1
                else:
                    r['d'] = haversine_distance(user_pos, (u.geo_lat, u.geo_lon))
                response.append(r)

        return HttpResponse(json.dumps(response), mimetype='application/json')


class UsersPrivacyView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(request.user.privacy()),
                            mimetype='application/json')

    @is_authenticated_or_401
    def put(self, request, *args, **kwargs):
        user = request.user

        #TODO Chequear y limpiar entradas
        name = PUT(request, 'name')
        if name: user.how_can_see_name = name

        bio = PUT(request, 'bio')
        if bio: user.how_can_see_bio = bio

        picture = PUT(request, 'picture')
        if picture: user.how_can_see_picture = picture

        age = PUT(request, 'age')
        if age: user.how_can_see_age = age

        ss = PUT(request, 'ss')
        if ss: user.how_can_see_ss = ss

        tel = PUT(request, 'tel')
        if tel: user.how_can_see_tel = tel

        email = PUT(request, 'email')
        if email: user.how_can_see_email = email

        user.save()
        resp = user.privacy()

        return HttpResponse(json.dumps(resp), mimetype='application/json')
