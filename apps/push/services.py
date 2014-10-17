from datetime import datetime
from datetime import timedelta
import json

from python_push.message import Message
from python_push.gcm.gcm_push_service import GCMPushService
from python_push.blackberry.bb_push_service import BBPushService
from python_push.parse_ai.parse_ai_push_service import ParseAIService
from python_push.push_manager import PushManager

from models import Device, Chunk


class BarachielPushManager:

    push_manager = PushManager([
        #TODO: Pasar estos datos a settings.py
        GCMPushService({'api_id': 'AIzaSyB5NvAZuGrhbpCVxszC6IESbHcYLBDtxz0'}),
        ParseAIService({'app_id': 'GwiELlzA5upc3gGjpzvbx4AW2CmMLNJd40vx14sz', 'rest_key': 'oSJtjfFZcqjNOZ5xWW2RjVUViIDaZ8B9J9LU7l9i'}),
        BBPushService({'api_id': '2974-Mie72996c2B7m3t87M17o8172i80r505273', 'password': 'dsvoolM5'}),
    ])

    message = None
    devices = None
    sync_data = None

    def __init__(self):
        self.devices = []
        self.sync_data = []
        self.message = Message()
        self.message.payload = {
            'type': 'osync'
        }

    def add_user(self, user):
        #Se puede optimizar para agregar listas de usuarios en lote desde la BD:
        new_devices = Device.objects.filter(user=user)
        self.devices += list(new_devices)

    def add_sync_data(self, data):
        chunk = Chunk(data=data, expiration=datetime.now() + timedelta(days=30))
        self.sync_data.append(chunk)

    def set_like(self, like):
        self.message.payload['type'] = 'like'
        self.message.payload['like_id'] = like.id
        self.add_user(like.liked)
        self.add_sync_data(json.dumps({
            # Wrapped Model:
            'model': like.serialize(like.liked),
            'class': 'Like'
        }))

        if(not like.anonymous):
            self.message.payload['user_name'] = like.liker.name[:16]
            self.message.set_option('alert',  {
                'loc-key': '%@ has Waved at you',
                'loc-args': [self.message.payload['user_name']]
            })
        else:
            self.message.set_option('alert', {
                'loc-key': 'Someone has sent you an anonymous wave.'
            })

    def send(self):
        import socket
        if len(self.devices) > 0:

            for chunk in self.sync_data:
                chunk.save()
                chunk.add_devices(self.devices)

            try:
                status_dict = self.push_manager.send(self.message, self.devices)
                print 'Sending push:\n'
                errors = []

                for type, status in status_dict.iteritems():
                    print '    Service %s: Status %i, Content="%s"\n' % (type, status.code, status.raw)
                    if not status.is_ok:
                        errors += (type, status.code, status.raw)

                if len(errors) > 0:
                    return errors
            except socket.error, e:
                print 'Push Service not found %s' % (e.strerror)
        else:
            print 'No devices to push.\n'

        return None
