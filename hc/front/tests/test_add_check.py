from hc.api.models import Check, Channel
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    def test_team_access_works(self):
        """
        Test that team access works
        This method tests if a check added by a user (bob) is accessed by another user (alice)
        who is on the same team
        :return:
        """

        # url to add a check
        url = "/checks/add/"

        # login bob and post the check to be added
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)

        # assert that the check was added
        assert Check.objects.count() == 1

        # retrieve the recently created check
        check = Check.objects.get()

        # url to the log of the recently added check
        url_check_log = "/checks/%s/log/" % check.code

        # Logging in as Alice, not Bob. Alice has team access so this
        # should work and he should access Bob's logs
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(url_check_log)

        # assert that Alice successfully sees Bob's check's logs
        self.assertEqual(r.status_code, 200)

    def test_team_access_doesnt_work_for_non_teams(self):
        """
        Test that team access doesn't work on users who do not belong to the same team
        This method tests if a check added by a user (bob) is not accessed by another user (charlie)
        who is not on the same team
        :return:
        """

        # url to add a check
        url = "/checks/add/"

        # login bob and post the check to be added
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)

        # assert that the check was added
        assert Check.objects.count() == 1

        # retrieve the recently created check
        check = Check.objects.get()

        # url to the log of the recently added check
        url_check_log = "/checks/%s/log/" % check.code

        # Logging in as Charlie, not Bob. Charlie has no team access so this
        # should not work and he should never access Bob's logs
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.get(url_check_log)

        # assert that Charlie gets a 403 when he tries to see Bob's check's logs
        self.assertEqual(r.status_code, 403)
