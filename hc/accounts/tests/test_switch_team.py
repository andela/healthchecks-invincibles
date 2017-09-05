from hc.test import BaseTestCase
from hc.api.models import Check


class SwitchTeamTestCase(BaseTestCase):
    """Test that users are able to switch to teams in which they are members"""
    def test_it_switches(self):
        """Assert that user can switch to a team where they is a member"""
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)

        ### Assert the contents of r
        self.assertEqual(r.context['checks'][0].name, "This belongs to Alice")


    def test_it_checks_team_membership(self):
        """Assert that user can't switch to a team since where he is not a member"""
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url)
        ### Assert the expected error code
        self.assertEqual(r.status_code, 403)

    def test_it_switches_to_own_team(self):
        """Assert that user can switch to their own team"""
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        ### Assert the expected error code
        self.assertEqual(r.status_code, 200)