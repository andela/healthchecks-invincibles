from django.contrib.auth.models import User
from django.test import TestCase
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):
    """Tests whether a profile can be added in association with a new user"""
    def test_it_handles_missing_profile(self):
        user = User(username="ned", email="ned@example.org")
        user.set_password("password")
        user.save()

        # Assert the new Profile objects count
        neds_profile = Profile(user=user)
        neds_profile.save()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(str(Profile.objects.get(user=user.id)), "ned@example.org")
        #  Assert if new user can log in
        self.client.login(username="ned@example.org", password="password")
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)