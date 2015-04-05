import json
from sys import maxint

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django_rq import enqueue

from libs.decorators import is_authenticated_or_401
from models import Like
from apps.users.models import User
from apps.push.services import BarachielPushManager


class LikesView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        user = request.user
        if user is None:
            return HttpResponseForbidden()
        # TODO: Security

        like = get_object_or_404(Like, id=kwargs['id'])

        response = like.serialize(request.user)

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    # DEPRECATED DELETE!!!!!!
    @is_authenticated_or_401
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

            # ---------****---  PUSH  ---****--------- #
            yg_pm = BarachielPushManager()
            yg_pm.set_like(like)
            yg_pm.send()

            return HttpResponse(json.dumps(response),
                                mimetype='application/json')

        except IntegrityError:
            # TODO si ya existe pero con anonymous distinto actualizar.
            return HttpResponseBadRequest("Already Waved")


class LikesListView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        user = request.user

        response = map(lambda l: l.preview(user), user.likes_to.all().order_by('_updated_at')[:100])

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')


class LikesFromView(View):
    @is_authenticated_or_401
    def delete(self, request, *args, **kwargs):
        user = request.user

        like = get_object_or_404(user.likes_from, id=kwargs['id'])
        print "deleting " + str(like)
        like.delete()

        response = like.serialize(request.user)

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')


def send_like(liker_id, liked_id, message, is_anonymous=False):
    user_liker = User.objects.get(id=liker_id)
    user_liked = User.objects.get(id=liked_id)

    already_waved = True
    like = None
    try:
        like = Like.objects.get(liker=user_liker, liked=user_liked)
        like.anonymous = is_anonymous

    except ObjectDoesNotExist:
        already_waved = False
        like = Like(
            liker=user_liker,
            liked=user_liked,
            anonymous=is_anonymous
        )

    like.save()
    if message:
        like.add_message(message)

    # ---------****---  PUSH  ---****--------- #
    yg_pm = BarachielPushManager()
    yg_pm.set_like(like)
    yg_pm.send()

    response = like.serialize(user_liker)
    return (response, already_waved)


class LikesFromListView(View):
    @is_authenticated_or_401
    def get(self, request, *args, **kwargs):
        user = request.user

        response = map(lambda l: l.preview(user), user.likes_from.all().order_by('_updated_at')[:100])

        return HttpResponse(json.dumps(response),
                            mimetype='application/json')

    @is_authenticated_or_401
    def post(self, request, *args, **kwargs):
        liker_id = request.user.id
        liked_id = int(request.POST.get('user_id'))
        is_anonymous = request.POST.get('anonym') == "true"
        message = request.POST.get('message')

        (response, already_waved) = send_like(liker_id, liked_id, message, is_anonymous)

        return HttpResponse(
            json.dumps(response),
            status=212 if already_waved else 200,
            mimetype='application/json'
        )


class LikesBroadcastView(View):
    @is_authenticated_or_401
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            HttpResponseForbidden()

        liker_id = request.user.id
        message = request.POST.get('message')
        min_id = request.POST.get('min_id', 0)
        max_id = request.POST.get('max_id', maxint)

        users = User.objects.filter(
            id__gte=min_id,
            id__lte=max_id,
        ).order_by('-last_login')

        for user in users:
            print "Enqueue Wave for user %s (%d)" % (str(user), user.id)
            enqueue(send_like, liker_id, user.id, message)

        return HttpResponse(
            '{} Waves enqueued.'.format(len(users)),
            status=200,
        )
