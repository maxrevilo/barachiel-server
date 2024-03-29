# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.views.generic import View
from django.shortcuts import get_object_or_404
from libs.helpers import get_client_ip
from libs.decorators import is_authenticated_or_401
from models import ReferrerProfile


class ReferralsListView(View):
    @is_authenticated_or_401
    def post(self, request, *args, **kwargs):
        referred_user = request.user
        client_IP = get_client_ip(request)
        referral_token = request.POST['token'].upper()

        try:
            referrer_profile = ReferrerProfile.objects.get(token=referral_token)
        except ReferrerProfile.DoesNotExist:
            return Http404('Referrer not found.')

        if not referrer_profile.active:
            return HttpResponseForbidden("This referrer has been disabled.")

        # referrer_user = referrer_profile.user
        referred = referrer_profile.refer_user(referred_user, client_IP)
        if referred is None:
            return HttpResponseBadRequest("Already referred by the specified user.")

        response = referred.serialize(request.user)

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    # def put(self, request, *args, **kwargs):
    # def delete(self, request, *args, **kwargs):
