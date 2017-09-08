from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


class CheckModelTestCase(TestCase):

    def test_it_strips_tags(self):
        """ Test for when check is a space separated string or an empty string, en empty string returns length 0"""
        check = Check()

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])

        check.tags = ""
        self.assertEqual(len(check.tags_list()), 0)

    def test_status_works_with_grace_period(self):
        """test for check status and the grace period"""
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())
        self.assertEqual(check.get_status(), "up")

    def test_paused_check_is_not_in_grace_period(self):
        """  Test that when a new check is created, it is not in the grace period"""
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
        self.assertFalse(check.in_grace_period())
