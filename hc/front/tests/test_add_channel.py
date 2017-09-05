from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    def test_team_access_works(self):
        """
        Test that the team access works
        This method aims at testing whether a channel created by a user (alice) can be accessed by
        another user (bob) who is on the same team
        :return:
        """

        # url for adding an integration
        url = "/integrations/add/"
        form = {"kind": "slack", "value": "our_team_slack_handle"}

        # login alice and post the channel to be created
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        # assert if the channel is created
        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

        # retrieve the recently created channel
        channel = Channel.objects.get(kind="slack")

        # url to access checks from the created channel. this is used to test access
        url_to_checks = "/integrations/%s/checks/" % channel.code

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")

        # bob trying to access the created channel
        r = self.client.get(url_to_checks)
        self.assertContains(r, "Assign Checks to Channel", status_code=200)

    def test_team_access_doesnt_work_for_non_teams(self):
        """
        Test that the team access doesn't work for users who are not on the same team
        This method aims at testing whether a channel created by a user (alice) can be accessed by
        another user (charlie) who is not on the same team
        :return:
        """

        # url for adding a channel
        url = "/integrations/add/"
        form = {"kind": "slack", "value": "our_team_slack_handle"}

        # login alice and post the channel to be created
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        # assert if the channel is created
        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

        # retrieve the recently created channel
        channel = Channel.objects.get(kind="slack")

        # url to access checks from the created channel. this is used to test access
        url_to_checks = "/integrations/%s/checks/" % channel.code

        # Logging in as charlie, not alice. Charlie has no team access so this
        # should not work.
        self.client.login(username="charlie@example.org", password="password")

        # bob trying to access the created channel. this should not work and 403 should be returned
        r = self.client.get(url_to_checks)
        self.assertNotContains(r, "Assign Checks to Channel", status_code=403)

    def test_it_fails_on_bad_channel_kind(self):
        """
        Test that bad kinds don't work
        This method tests that a channel that is not in the expected list of channels is not created when a user tries
        to add it
        :return:
        """

        # url for adding a channel
        url = "/integrations/add/"

        # whatsapp is a bad channel and is not expected as per supported channels
        form = {"kind": "whatsapp", "value": "alice"}

        # login alice and post the bad channel to be created
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        # assert that a bad request status code is returned
        self.assertEqual(r.status_code, 400)
