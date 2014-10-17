from django.test import TestCase
from apps.users.models import User
from django.core import mail


class ModuleBaseTest(TestCase):
    fixtures = ['user.json', 'confirmation.json']

    def setUp(self):
        self.user = User.objects.get(email='test1@t.com')
        logged = self.client.login(username=self.user.email, password='1234')
        if logged is False:
            raise Exception("Test User not logged")


class UserTest(ModuleBaseTest):

    def setUp(self):
        super(UserTest, self).setUp()

    def test_send_confirmation_reminder_mail_basic(self):
        self.user.send_confirmation_reminder_mail()
        #TODO: Be more specific
        self.assertEqual(len(mail.outbox), 1)

    def test_send_confirmation_mail_basic(self):
        self.user.send_confirmation_mail(True)
        #TODO: Be more specific
        self.assertEqual(len(mail.outbox), 1)
