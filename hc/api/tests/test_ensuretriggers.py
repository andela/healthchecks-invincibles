from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from hc.api.management.commands.ensuretriggers import Command
from hc.api.models import Check


class EnsureTriggersTestCase(TestCase):

    def test_ensure_triggers(self):
        """Assert that alert_after is lesser than the check's alert_after"""
        Command().handle()

        check = Check.objects.create()
        assert check.alert_after is None

        check.last_ping = timezone.now()
        check.save()
        check.refresh_from_db()
        assert check.alert_after is not None
<<<<<<< HEAD

=======
        
>>>>>>> test(EnsureTriggers): test for alert before and after trigger
        alert_after = check.alert_after
        check.last_ping += timedelta(days=1)
        check.save()
        check.refresh_from_db()
        self.assertLess(alert_after, check.alert_after)
<<<<<<< HEAD
=======
        
>>>>>>> test(EnsureTriggers): test for alert before and after trigger
