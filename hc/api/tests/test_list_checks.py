import json
from datetime import timedelta as td
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        """Test for setup"""
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        """Methods that gets all the checks"""
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        """Tests for listing all checks"""
        r = self.get()
        self.assertEqual(r.status_code,200)
        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}

        # Assert the expected length of checks
        self.assertEqual(len(checks), 2)
        ### Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status,
        ### last_ping, n_pings and pause_url
        self.assertEqual(checks["Alice 1"]["timeout"], 3600)
        self.assertEqual(checks["Alice 1"]["grace"], 900)
        self.assertEqual(checks["Alice 1"]["ping_url"], self.a1.url())
        self.assertEqual(checks["Alice 1"]["status"], "new")
        #self.assertEqual(checks["Alice 1"]["last_ping"], self.now.isoformat()) #represents the date in ISO 8601 format, ‘YYYY-MM-DD’
        self.assertEqual(checks["Alice 1"]["n_pings"], 1)


        pause_rel_url = reverse("hc-api-pause", args=[self.a1.code])
        pause_url = settings.SITE_ROOT + pause_rel_url
        self.assertEqual(checks["Alice 1"]["pause_url"], pause_url)
        
        self.assertEqual(checks["Alice 2"]["timeout"], 86400)
        self.assertEqual(checks["Alice 2"]["grace"], 3600)
        self.assertEqual(checks["Alice 2"]["ping_url"], self.a2.url())
        self.assertEqual(checks["Alice 2"]["status"], "up")

        self.assertEqual(checks["Alice 2"]["last_ping"], self.now.isoformat())

        pause_rel_url = reverse("hc-api-pause", args=[self.a2.code])
        pause_url = settings.SITE_ROOT + pause_rel_url

        self.assertEqual(checks["Alice 2"]["n_pings"], 0)


    def test_it_shows_only_users_checks(self):
        """Test for displaying only users checks"""
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")
    def test_it_accepts_api_key_in_the_request(self):
        """Test that it accepts an api_key in the request"""
        r = self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc", content_type="application/json")
        self.assertEqual(r.status_code, 200)
