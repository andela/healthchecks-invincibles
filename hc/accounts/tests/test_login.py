from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):
    """Tests to ensure that the login procedure works"""
    def test_it_sends_link(self):
        # create a new check and
        # reference the code to old_code that identifies the check
        check = Check()
        check.save()
        old_code = check.code

        # create a welcome code attribute to session and equate it to check.code
        # this is used in associating the new user to the demo check
        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}
        # Assert that it should redirect to checks after login
        response = self.client.post("/accounts/login/", form)
        assert response.status_code == 302

        # Assert that a user was created during the login process
        user = User.objects.get(email="alice@example.org")
        self.assertEqual(user.email, "alice@example.org")

        # Assert that an email, containing the log in link is sent when a new user is created
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')

        # Assert contents of the email body
        assert "To log into healthchecks.io" in mail.outbox[0].body

        # Assert that check is associated with the new user
        # if old-check is equivalent to the code of the check associated the user_id,
        # then the check is associated with the new user.
        self.assertTrue(Check.objects.get(user_id=user.id))
        self.assertEqual(old_code, Check.objects.get(user_id=user.id).code)


    def test_it_pops_bad_link_from_session(self):
        # if bad_link is in session, a get request to "/accounts/login/" should clear this attribute
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session


