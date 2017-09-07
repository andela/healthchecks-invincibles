from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        # Assert the expected status code and check's status
        self.assertEqual(r.status_code, 200)
        self.assertEqual(check.status, "up")

    def test_it_validates_ownership(self):
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(r.status_code, 400)

    def test_allows_only_post_request(self):
        """Test that it only allows post requests"""
        url = "/api/v1/checks/1659718b-21ad-4ed1-8740-43afc6c41524/pause"
        r = self.client.get(url, HTTP_X_API_KEY="abc")
        self.assertEqual(r.status_code, 405)
