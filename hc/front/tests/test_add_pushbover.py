from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    def test_it_adds_channel(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=n&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r.status_code == 302

        channels = list(Channel.objects.all())
        assert len(channels) == 1
        assert channels[0].value == "a|0"

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/integrations/add_pushover/")
        self.assertEqual(r.status_code, 404)

    def test_it_validates_nonce(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r.status_code == 403

    def test_pushover_validates_invalid_priority(self):
        """
        Test to validate that if the passed priority value is not between -2 to 2,
        it should fail with a BadRequestError 
        """
        # Login Alice
        self.client.login(username="alice@example.org", password="password")

        # Initiate a session
        session = self.client.session
        # Create and store a nonce in the session, which will be part of the params 
        session["po_nonce"] = "n"
        session.save()

        # Pass the correct 'pushover_user_key' and 'nonce' but pass an 'invalid priority',
        # to create an incorrect params
        params = "pushover_user_key=a&nonce=n&prio=INVALID"
        r = self.client.get("/integrations/add_pushover/?%s" % params)

        # Accessing the '/integrations/add_pushover/params' url should fail with a BadRequestError
        assert r.status_code == 400

    def test_pushover_validates_correct_priority(self):
        """
        Test to check that a correct priority value passes 
        """
        # Login Alice
        self.client.login(username="alice@example.org", password="password")

        # Initiate a session
        session = self.client.session
        # Create and store a nonce in the session, which will be part of the params 
        session["po_nonce"] = "n"
        session.save()

        # Pass all correct values for the 'pushover_user_key', 'nonce' and 'priority',
        # to create an correct params
        params = "pushover_user_key=a&nonce=n&prio=2"
        r = self.client.get("/integrations/add_pushover/?%s" % params)

        # Accessing the '/integrations/add_pushover/params' url should redirect successfully
        assert r.status_code == 302