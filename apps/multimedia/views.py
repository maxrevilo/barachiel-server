import json
# from django.conf import settings
# import os

from django.http import HttpResponse  # , HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic import View
# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist

from models import Media
from libs.decorators import is_authenticated_or_401


# class MediaInstance(View):
#     def delete(self, request, *args, **kwargs):
#         media = get_object_or_404(Media, id=kwargs['id'])
#         message = get_object_or_404(Message, picture=media)
#         group = message.chat.group.all()[:1][0]
#         try:
#             membership_user = group.memberships.get(user=(request.user))
#         except ObjectDoesNotExist:
#                 return HttpResponseForbidden()

#         if membership_user.can_delete_media() or request.user.id == media.uploader.id:
#             media.delete()
#             path = os.path.join(settings.MEDIA_ROOT, str(media.file))
#             try:
#                 os.remove(path)
#                 print path
#             except OSError:
#                 pass
#             return HttpResponse()
#         else:
#             return HttpResponseForbidden()

class MediaUser(View):
    @is_authenticated_or_401
    def post(self, request, *args, **kwargs):
        user = request.user
        media = Media.from_request(request, user)

        if media is None:
            return HttpResponse(status=413)

        resp = media.preview(user)
        return HttpResponse(json.dumps(resp), mimetype='application/json')
