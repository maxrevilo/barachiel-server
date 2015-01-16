import json

from django.test import TestCase

from apps.referrals.models import Referred
from apps.users.models import User


class ReferralsBaseTest(TestCase):
    fixtures = ['user.json', 'referrals.json', ]
    referred_user = None
    referrer_user = None
    referrer_profile = None
    client_ip = '127.0.0.1'

    def setUp(self):
        self.referrer_user = User.objects.get(email='test1@t.com')
        self.referrer_profile = self.referrer_user.referrer_profile
        self.referred_user = User.objects.get(email='test3@t.com')
        logged = self.client.login(username=self.referred_user.email, password='1234')
        if logged is False:
            raise Exception("Test User not logged")

    def accept_post_only(self):
        methods = ('get', 'put', 'options', 'delete')
        for method in methods:
            response = getattr(self.client, method)(self.url, self.params)
            self.assertEqual(response.status_code, 405)


class ReferredByReferrerTest(ReferralsBaseTest):
    url = '/referrals/'

    def setUp(self):
        super(ReferredByReferrerTest, self).setUp()

    def test_referred_by_referrer(self):
        params = {
            'token': self.referrer_profile.token
        }
        refereds_count_before = self.referrer_profile.referrals.count()

        response = self.client.post(self.url, params)
        referred_json = json.loads(response.content)
        referred = Referred.objects.get(pk=referred_json["id"])
        refereds_count_after = self.referrer_profile.referrals.count()

        #This verifies that the respose belong to the 2xx family
        self.assertEqual(response.status_code/100, 2)
        self.assertEqual(referred_json["user"]["id"], self.referred_user.pk)
        self.assertEqual(referred_json["referrer"]["id"], self.referrer_profile.id)
        self.assertFalse(referred.accepted)
        self.assertEqual(referred.referrer.id, self.referrer_profile.id)
        self.assertEqual(referred.IP, self.client_ip)
        self.assertEqual(refereds_count_before, refereds_count_after - 1)

    def test_referred_by_deactivated_referrer(self):
        self.referrer_profile.active = False
        self.referrer_profile.save()

        params = {
            'token': self.referrer_profile.token
        }
        refereds_count_before = self.referrer_profile.referrals.count()

        response = self.client.post(self.url, params)
        refereds_count_after = self.referrer_profile.referrals.count()

        self.assertEqual(response.status_code, 403)
        self.assertTrue(refereds_count_before == refereds_count_after)

    def test_referred_by_referrer_twice(self):
        params = {
            'token': self.referrer_profile.token
        }
        refereds_count_before = self.referrer_profile.referrals.count()

        # The first request, should be ok:
        response = self.client.post(self.url, params)
        refereds_count_after = self.referrer_profile.referrals.count()

        #This verifies that the respose belong to the 2xx family
        self.assertEqual(response.status_code/100, 2)
        self.assertEqual(refereds_count_before, refereds_count_after - 1)

        # The second request, should return 400:
        response = self.client.post(self.url, params)
        refereds_count_before = refereds_count_after
        refereds_count_after = self.referrer_profile.referrals.count()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(refereds_count_before, refereds_count_after)

    def test_not_logged_referred(self):
        self.client.logout()

        params = {
            'token': self.referrer_profile.token
        }
        refereds_count_before = self.referrer_profile.referrals.count()

        response = self.client.post(self.url, params)
        refereds_count_after = self.referrer_profile.referrals.count()

        self.assertEqual(response.status_code, 401)
        self.assertTrue(refereds_count_before == refereds_count_after)
