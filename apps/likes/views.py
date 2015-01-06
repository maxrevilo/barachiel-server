import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from libs.decorators import login_required_or_403
from django.db import IntegrityError

from models import Like
from apps.users.models import User
from apps.push.services import BarachielPushManager


class LikesView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return HttpResponseForbidden()
        #TODO: Security

        like = get_object_or_404(Like, id=kwargs['id'])

        response = like.serialize(request.user)

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    # DEPRECATED DELETE!!!!!!
    def post(self, request, *args, **kwargs):
        user_liker = request.user
        user_liked = get_object_or_404(User, id=kwargs['id'])

        try:
            like = Like(
                liker     =user_liker,
                liked     =user_liked,
                anonymous =request.POST.get('anonym') == "true"
            )
            like.save()

            response = like.serialize(user_liker)

            #---------****---  PUSH  ---****---------#
            yg_pm = BarachielPushManager()
            yg_pm.set_like(like)
            yg_pm.send()

            return HttpResponse(json.dumps(response),
                                mimetype='application/json')

        except IntegrityError:
            #TODO si ya existe pero con anonymous distinto actualizar.
            return HttpResponseBadRequest("Already Waved")

    #def put(self, request, *args, **kwargs):
    #def delete(self, request, *args, **kwargs):


class LikesListView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return HttpResponseForbidden()

        response = map(lambda l: l.preview(user), user.likes_to.all()[:100])

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    def post(self, request, *args, **kwargs):
        user_liker = request.user
        user_liked = get_object_or_404(User, id=request.POST['user_id'])

        try:
            like = Like(
                liker     =user_liker,
                liked     =user_liked,
                anonymous =request.POST.get('anonym') == "true"
            )
            like.save()

            response = like.serialize(user_liker)

            #---------****---  PUSH  ---****---------#
            yg_pm = BarachielPushManager()
            yg_pm.set_like(like)
            yg_pm.send()

            return HttpResponse(json.dumps(response),
                                mimetype='application/json')

        except IntegrityError:
            #TODO si ya existe pero con anonymous distinto actualizar.
            return HttpResponseBadRequest("Already Waved")
