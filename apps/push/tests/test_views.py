import json
from datetime import datetime
from datetime import timedelta
from random import choice
from string import lowercase

from django.test import TestCase

from apps.push.models import Chunk, Device
from apps.users.models import User


class PushBaseTest(TestCase):
    fixtures = ['user.json', 'devices.json', ]
    params = None
    user = None
    device = None

    def setUp(self):
        self.user = User.objects.get(email='test1@t.com')
        logged = self.client.login(username=self.user.email, password='1234')
        if logged is False:
            raise Exception("Test User not logged")

        self.device = Device.objects.get(user=self.user)
        self.params = {'id': self.device.pk}

    def accept_post_only(self):
        methods = ('get', 'put', 'options', 'delete')
        for method in methods:
            response = getattr(self.client, method)(self.url, self.params)
            self.assertEqual(response.status_code, 405)


class SubscribeTest(PushBaseTest):
    url = '/push/subscribe/'
    base_params = None

    def setUp(self):
        super(SubscribeTest, self).setUp()
        self.base_params = self.params
        self.base_user = self.user

        self.user = User.objects.get(email='test2@t.com')
        logged = self.client.login(username=self.user.email, password='1234')
        if logged is False:
            raise Exception("Test User 2 not logged")

        self.params = {
            'token': 'Android Token 2',
            'type': 'GA',
        }

    def test_accept_post_only(self):
        self.accept_post_only()

    def test_new_device_subscription(self):
        response = self.client.post(self.url, self.params)
        device = Device.objects.get(user=self.user)
        device_json = json.loads(response.content)

        #This verifies that the respose belong to the 2xx family
        self.assertEqual(response.status_code/100, 2)
        self.assertEqual(device_json["id"], device.pk)
        self.assertEqual(device_json["type"], self.params["type"])

    def test_existent_device_subscription(self):
        response = self.client.post(self.url, self.params)
        device_json = json.loads(response.content)
        # The second time
        response2 = self.client.post(self.url, self.params)
        device_json2 = json.loads(response2.content)

        self.assertEqual(response.status_code/100, 2)
        self.assertEqual(device_json["id"], device_json2["id"])

    def test_user_shouldnt_unsubscribe_other_users_device(self):
        bad_hacker = User.objects.get(email='test2@t.com')
        logged = self.client.login(username=bad_hacker.email, password='1234')
        if logged is False:
            raise Exception("Test User 2 not logged")

        #self.params have the id of the test1@t.com device.
        response = self.client.post(self.url, {
            'token': self.device.token,
            'type': self.device.type,
        })

        self.assertEqual(response.status_code, 400)


class UnsubscribeTest(PushBaseTest):
    url = '/push/unsubscribe/'

    def test_accept_post_only(self):
        self.accept_post_only()

    def test_user_shouldnt_unsubscribe_other_users_device(self):
        bad_hacker = User.objects.get(email='test2@t.com')
        logged = self.client.login(username=bad_hacker.email, password='1234')
        if logged is False:
            raise Exception("Test User 2 not logged")

        #self.params have the id of the test1@t.com device.
        response = self.client.post(self.url, self.params)

        self.assertEqual(response.status_code, 404)


class SyncTest(PushBaseTest):
    url = '/push/sync/'

    def test_accept_post_only(self):
        self.accept_post_only()

    def test_correct_sync(self):
        response = self.client.post(self.url, self.params)
        #This verifies that the respose belong to the 2xx family
        self.assertEqual(response.status_code/100, 2)

    def test_empty_sync(self):
        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, 204)

    def test_sync_with_one_chunk(self):
        data = "test data"
        chunk = Chunk(data=data, expiration=datetime.now() + timedelta(days=30))
        chunk.save()
        chunk.add_devices([self.device])

        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data[0], data)

    def test_sync_with_large_chunk(self):
        size = 1000000  # Le million
        data = "".join(choice(lowercase) for i in range(size))
        chunk = Chunk(data=data, expiration=datetime.now() + timedelta(days=30))
        chunk.save()
        chunk.add_devices([self.device])

        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data[0], data)

    def test_sync_with_many_chunks(self):
        rg = range(10, 23)
        data_tpl = "data %d"
        for i in rg:
            chunk = Chunk(data=data_tpl % i, expiration=datetime.now() + timedelta(days=30))
            chunk.save()
            chunk.add_devices([self.device])

        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)
        self.assertEqual(len(json_data), len(rg))

        #The order must be preserved
        for i in range(len(rg)):
            self.assertEqual(json_data[i], data_tpl % rg[i])

    def test_update_device_last_sync(self):
        last_sync = self.device.last_sync
        response = self.client.post(self.url, self.params)
        #This verifies that the respose belong to the 2xx family
        self.assertEqual(response.status_code/100, 2)
        self.device = Device.objects.get(user=self.user)
        self.assertGreater(self.device.last_sync, last_sync)

    def test_user_shouldnt_sync_other_users_device(self):
        bad_hacker = User.objects.get(email='test2@t.com')
        logged = self.client.login(username=bad_hacker.email, password='1234')
        if logged is False:
            raise Exception("Test User 2 not logged")

        #self.params have the id of the test1@t.com device.
        response = self.client.post(self.url, self.params)

        self.assertEqual(response.status_code, 404)
