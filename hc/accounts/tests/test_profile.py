from django.core import mail

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):
    """
    Test functionality in profile view
    """
    def test_it_sends_set_password_link(self):
        """
        tests whether an email is containing the reset password link when set password is chosen
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token

        # Assert that the token is set
        self.assertEqual(len(token), 49)

        # Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Set password on healthchecks.io')
        assert "Here's a link to set a password for your account" in mail.outbox[0].body

    def test_it_sends_report(self):
        """
        Test whether an email containing the reports is sent when send report function is called.
        """
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        # Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Monthly Report')
        assert "This is a monthly report sent by healthchecks.io." in mail.outbox[0].body

    def test_it_adds_team_member(self):
        """Test that only team owners can invite other users to their teams"""
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        # Assert the existence of the member emails
        self.assertGreater(len(member_emails), 0)
        # Assert that frank@example.org is part of the member emails
        self.assertTrue("frank@example.org" in member_emails)

        # Assert that the invitation email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         "You have been invited to join alice@example.org on healthchecks.io")
        assert "You will be able to manage their existing" in mail.outbox[0].body

    def test_add_team_member_checks_team_access_allowed_flag(self):
        """
        Assert that only a team member can invite someone to the team
        """
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        """
        Assert that only the owner of the team can remove someone from the team
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        """
        Assert that only the owner of the team can set the team name
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        """
        Assert that a non team member cannot set the name of the team
        """
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")


    def test_creates_API_key(self):
        """ Test it creates API key """
        self.client.login(username="alice@example.org", password="password")
        form = {"create_api_key": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200
        messages = list(r.context['messages'])
        self.assertEqual(str(messages[0]), "The API key has been created!")

    def test_revokes_API_key(self):
        """# Test it revokes API key"""
        self.client.login(username="alice@example.org", password="password")
        form = {"revoke_api_key": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200
        messages = list(r.context['messages'])
        self.assertEqual(str(messages[0]), "The API key has been revoked!")
