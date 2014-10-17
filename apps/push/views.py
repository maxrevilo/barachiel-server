import json

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import FieldError
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from libs.decorators import login_required_or_403
from models import Device


@login_required_or_403
def subscribe(request):
    # POST CHECKINGS:
    if request.method != 'POST':
        return HttpResponseNotAllowed('POST')
    token_r = None
    type_r = None
    try:
        token_r = request.POST['token']
        type_r = request.POST['type']
    except MultiValueDictKeyError:
        return HttpResponseBadRequest('POST must contain "token" and "type"')
    # END OF POST CHECKINGS:

    device = None
    try:
        device = Device(
            user=request.user,
            token=token_r,
            type=type_r)
        with transaction.atomic():
            device.save()

    except IntegrityError:
        try:
            device = request.user.devices.get(token=token_r, type=type_r)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("A device with that token is already used by other user.")

    except FieldError:
            return HttpResponseBadRequest('Incorrect "type" value.')

    return HttpResponse(json.dumps(device.preview(user=request.user)),
                             mimetype='application/json')


@login_required_or_403
def unsubscribe(request):
    # POST CHECKINGS:
    if request.method != 'POST':
        return HttpResponseNotAllowed('POST')
    id_r = None
    try:
        print 'push unsubscribe id: '+request.POST['id']

        id_r = int(request.POST['id'])
    except MultiValueDictKeyError:
        return HttpResponseBadRequest('POST must contain "id"')
    # END OF POST CHECKINGS:

    try:
        device = request.user.devices.get(id=id_r)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    device.delete()
    return HttpResponse(status=202)


@login_required_or_403
def sync(request):
    # POST CHECKINGS:
    if request.method != 'POST':
        return HttpResponseNotAllowed('POST')
    id_r = None
    try:
        id_r = request.POST['id']
    except MultiValueDictKeyError:
        return HttpResponseBadRequest('POST must contain "id"')
    # END OF POST CHECKINGS:

    """A device ask for data waiting to be sync"""
    try:
        device = request.user.devices.get(id=id_r)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    device.save()
    chunks = device.chunks.all()[:20]

    if len(chunks) > 0:
        user = request.user
        result = []
        for chunk in chunks:
            result.append(chunk.preview(user)['data'])
            chunk.remove_device(device)

        return HttpResponse(json.dumps(result), mimetype='application/json')
    else:
        return HttpResponse(status=204)

# from apps.likes.models import Like
# from apps.push.services import BarachielPushManager
# import datetime


# @login_required_or_403
# def test_push(request):
#     if request.user.is_admin is False:
#         return HttpResponseNotFound()

#     # POST CHECKINGS:
#     if request.method != 'POST':
#         return HttpResponseNotAllowed('POST')

#     try:
#         id_r = request.POST['id']
#     except MultiValueDictKeyError:
#         return HttpResponseBadRequest('POST must contain "id"')

#     """The device to send the push"""
#     try:
#         device = Device.objects.get(id=id_r)
#     except ObjectDoesNotExist:
#         return HttpResponseNotFound('Device not found id={}'.format(id_r))

#     like = Like(
#         liker=request.user,
#         liked=device.user,
#         anonymous=True if request.POST.get('annoym') is not None else False
#     )
#     like._created_at = datetime.datetime.now()

#     #---------****---  PUSH  ---****---------#
#     yg_pm = BarachielPushManager()
#     yg_pm.set_like(like)
#     yg_pm.send()

#     return HttpResponse(status=200)
