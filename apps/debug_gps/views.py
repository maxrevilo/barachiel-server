# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404

#from libs.helpers import PUT, change_in_latitude, change_in_longitude, haversine_distance
from models import Position
from apps.users.models import User
from libs.decorators import is_authenticated_or_401


class PositionView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        position = get_object_or_404(Position, id=kwargs['id'])

        return HttpResponse(json.dumps(position.serialize(request.user)),
                            mimetype='application/json')


class PositionsView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):

        defaults = {
            'user_id': None,

            'max_date_diff': 5,
            'min_date_diff': 0,

            'lat_max': float("inf"),
            'lat_min': float("-inf"),
            'lon_max': float("inf"),
            'lon_min': float("-inf"),

            'max': 512,
        }

        defaults.update(request.GET.dict())

        query = Position.objects\
                .filter(
                    #Filter by expiry
                    timestamp__gt=datetime.now() - timedelta(hours=float(defaults['max_date_diff'])),
                    timestamp__lt=datetime.now() - timedelta(hours=float(defaults['min_date_diff'])),

                    # #Filter by geolocation
                    lat__gte=float(defaults['lat_min']),
                    lat__lte=float(defaults['lat_max']),
                    lon__gte=float(defaults['lon_min']),
                    lon__lte=float(defaults['lon_max']),
                )

        if defaults['user_id'] is not None:
            user = get_object_or_404(User, id=int(defaults['user_id']))
            query = query.filter(user=user)

        query = query[:int(defaults['max'])]

        response = map(lambda p: p.preview(request.user), query)

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    @is_authenticated_or_401
    def post(self, request, *args, **kwargs):

        defaults = {
            "lat": None,  # Required
            "lon": None,  # Required
            "alt": None,
            "speed": None,
            "heading": None,
            "accuracy": None,
            "alt_accuracy": None,
            "timestamp": None,
            "device_type": None,
            "app_version": 0,
            "extra": None,
        }

        defaults.update(request.POST.dict())

        if defaults["timestamp"] is None:
            defaults["timestamp"] = datetime.now()
        else:
            defaults["timestamp"] = datetime.fromtimestamp(float(defaults["timestamp"]) / 1e3)

        def float_or_none(val):
            if val is not None:
                val = float(val)
            return val

        p = Position(
            user=request.user,
            lat=float_or_none(defaults["lat"]),
            lon=float_or_none(defaults["lon"]),
            alt=float_or_none(defaults["alt"]),
            speed=float_or_none(defaults["speed"]),
            heading=float_or_none(defaults["heading"]),
            accuracy=float_or_none(defaults["accuracy"]),
            alt_accuracy=float_or_none(defaults["alt_accuracy"]),
            timestamp=defaults["timestamp"],
            device_type=defaults["device_type"],
            app_version=defaults["app_version"],
            extra=defaults["extra"],
        )

        p.save()

        return HttpResponse(json.dumps(p.serialize(request.user)),
                            mimetype='application/json')
