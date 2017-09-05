from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):
    """Tests to check whether a user can be authenticated using their tokens"""
    def setUp(self):
        # user alice's profile is given a token of 'secret-key'
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        # test whether 'secret-key' token can be used to login Alice
        response = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(response, "You are about to log in")

    def test_it_redirects(self):
        # test whether it redirects to '/checks/' when 'secret-key' token is used to login Alice
        response = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_check_redirect_when_logged_in(self):
        # Login and test it redirects already logged in
        response = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

    def test_check_redirects_with_bad_token(self):
        # Login with a bad token and check that it redirects to Login page
        response = self.client.post("/accounts/check_token/alice/bad-link/")
        self.assertRedirects(response, "/accounts/login/")



