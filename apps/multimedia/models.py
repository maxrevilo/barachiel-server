#file: multimedia/models.py
# import os
import uuid
from django.db import models
# from django.conf import settings
from sorl.thumbnail import get_thumbnail
from time import mktime
# import random


class Media(models.Model):
    """Model for storing uploaded media"""

    TYPE_IMAGE = 'I'
    TYPE_VIDEO = 'V'
    TYPE_SOUND = 'S'

    TYPES = (
        (TYPE_IMAGE, 'Image'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_SOUND, 'Sound'),
    )

    uploader = models.ForeignKey('users.User', related_name='uploads')
    file = models.FileField(upload_to='uploaded/')
    type = models.CharField(choices=TYPES, max_length=1, default=TYPE_IMAGE)

    #Server data
    _created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-_created_at']

    # def update_filename(instance, filename):
    #     path = "uploaded/"
    #     format = instance.id + instance.transaction_uuid + instance.file_extension
    #     return os.path.join(path, format)

    @staticmethod
    def from_request(request, model):
        if request.FILES is None or len(request.FILES) == 0:
            return None

        media = Media(
            file=request.FILES[u'file'],
            uploader=request.user
        )
        # TODO: Append file extension or convert the image to jpg.
        media.file.name = str(uuid.uuid4())
        # media.save()

        # oldname = media.file.name
        # oldnamelist = oldname.split('/')
        # modelname = model.__class__.__name__
        # newname = oldnamelist[0] + '/' + modelname + '_' + str(model.id) + '_' + str(media.id) + '_' + oldnamelist[1]

        # os.rename(os.path.join(settings.MEDIA_ROOT, oldname), os.path.join(settings.MEDIA_ROOT, newname))
        # media.file.name = newname
        # media.save()

        if media.file.size > 10e6:
            return None
        else:
            media.save()

            # TODO: https://trello.com/c/uy6vBliW
            # if model.picture is not None:
            #     path = os.path.join(settings.MEDIA_ROOT, str(model.picture.file))
            #     try:
            #         os.remove(path)
            #         print path
            #     except OSError:
            #         pass
            #     old_instance = Media.objects.get(id=model.picture.id)
            #     old_instance.delete()

            model.picture = media
            model.save()

            return media

    def preview(self, user):
        from django.core.files.storage import default_storage as storage

        fh = storage.open(self.file.name, "w")

        # file_path = self.file.url

        result = {
            "id": self.pk,
            "type": self.type,
            "xLit": get_thumbnail(fh, "80x80", crop='center', quality=90).url,
            "xBig": get_thumbnail(fh, "1080x1080", crop='center').url,
            "xFull": self.file.url,
            "uploader_id": self.uploader.id
        }

        # from django.core.files import File
        # img_file = self.file
        # if self.type == Media.TYPE_IMAGE:
        #     img_file = File(open(self.file.path))
        # else:
        #     img_file = File(open(self.file.path.replace(".webm", ".png")))

        # result["x128"] = get_thumbnail(img_file, "128x128", crop='center', quality=80).url

        return result

    def serialize(self, user):
        return dict(self.preview(user), **{
            # "name": self.filename,
            "uploader": self.uploader.preview(user),
            "size": self.file.size,
            "date": int(mktime(self.date.timetuple()) * 1000),
        })

    def __unicode__(self):
        return self.file.name
