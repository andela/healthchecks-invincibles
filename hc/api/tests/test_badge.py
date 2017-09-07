from django.conf import settings
from django.core.signing import base64_hmac

from hc.api.models import Check
from hc.test import BaseTestCase


class BadgeTestCase(BaseTestCase):

    def setUp(self):
        super(BadgeTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

    def test_it_rejects_bad_signature(self):
        """ Assert for status code 400 """
        
        response = self.client.get("/badge/%s/12345678/foo.svg" % self.alice.username)
        self.assertEqual(response.status_code, 400)

    def test_it_returns_svg(self):
        """Assert that the svg is returned if the response status code is 200"""
        
        sig = base64_hmac(str(self.alice.username), "foo", settings.SECRET_KEY)
        sig = sig[:8].decode("utf-8")
        url = "/badge/%s/%s/foo.svg" % (self.alice.username, sig)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
