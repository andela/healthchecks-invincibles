from hc.api.models import Channel, Check
from hc.test import BaseTestCase
from django.contrib.auth.models import User


class ApiAdminTestCase(BaseTestCase):

    def setUp(self):
        super(ApiAdminTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

    def test_set_alice_as_superuser_and_staff(self):
        """Update user permission to superuser and staff"""

        User.objects.filter(username=self.alice).update(is_superuser=True, is_staff=True)
        self.alice = User.objects.get(id=self.alice.id)
        self.assertEqual(self.alice.is_superuser, True)
        self.assertTrue(self.alice.is_staff)

    def test_it_shows_channel_list_with_pushbullet(self):
        """Test for successful creation of Channel, with kind field"""

        self.client.login(username="alice@example.org", password="password")

        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()
        fetch_channel = Channel.objects.get(user=self.alice)
        self.assertEqual(fetch_channel.kind, 'pushbullet')
