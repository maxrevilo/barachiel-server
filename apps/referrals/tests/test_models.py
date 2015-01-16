from django.test import TestCase
from apps.users.models import User
from apps.referrals.models import ReferrerProfile, Referred


class ModuleBaseTest(TestCase):
    fixtures = ['user.json', 'referrals.json', ]
    referrer_profile = None
    referred_user = None
    client_ip = '192.0.0.1'

    def setUp(self):
        self.referrer_profile = ReferrerProfile.objects.get(pk=1)
        self.user = self.referrer_profile.user

        self.referred_user = User.objects.get(email='test3@t.com')


class ReferrerProfileTest(ModuleBaseTest):
    user2 = None
    referrer_profile2 = None

    def setUp(self):
        self.referrer_profile2 = ReferrerProfile.objects.get(pk=2)
        self.user2 = self.referrer_profile2.user
        super(ReferrerProfileTest, self).setUp()

    def test_refer_user(self):
        referred = self.referrer_profile.refer_user(
            self.referred_user,
            self.client_ip
        )

        self.assertIsNotNone(referred)
        self.assertEqual(referred.user.id, self.referred_user.id)
        self.assertEqual(referred.IP, self.client_ip)
        self.assertEqual(referred.referrer.id, self.referrer_profile.id)
        self.assertFalse(referred.accepted)

        #Just... don't throw anything
        self.referrer_profile.referrals.get(pk=referred.id)

    def test_refer_user_twice(self):
        referred = self.referrer_profile.refer_user(
            self.referred_user,
            self.client_ip
        )

        self.assertIsNotNone(referred)

        #Just... don't throw anything
        self.referrer_profile.referrals.get(pk=referred.id)

        # The second time should return None
        referred2 = self.referrer_profile.refer_user(
            self.referred_user,
            self.client_ip
        )
        self.assertIsNone(referred2)

    def test_refer_user_by_two_referrers(self):
        referred = self.referrer_profile.refer_user(
            self.referred_user,
            self.client_ip
        )

        self.assertIsNotNone(referred)

        #Just... don't throw anything
        self.referrer_profile.referrals.get(pk=referred.id)

        # The second time should return None
        referred2 = self.referrer_profile2.refer_user(
            self.referred_user,
            self.client_ip
        )
        self.assertIsNone(referred2)

    def test_accepted_referrals(self):
        count_before = self.referrer_profile.accepted_referrals_count()

        self.assertEqual(count_before, 1)
        referred2 = Referred.objects.get(pk=2)
        referred2.accepted = True
        referred2.save()

        count_after = self.referrer_profile.accepted_referrals_count()
        self.assertEqual(count_before, count_after - 1)
