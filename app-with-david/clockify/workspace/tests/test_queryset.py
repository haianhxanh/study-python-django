import django.utils.timezone
import struct
from tracemalloc import start
from django.forms import NullBooleanField
from django.test import TestCase
from unittest.mock import patch, Mock
from pprint import pprint
from time import strftime, gmtime, strptime
from workspace.models import TimeRecord, User
import datetime
from time import strftime, gmtime, struct_time
from django.utils import timezone
from workspace.querysets import TimeRecordQuerySet


class TimeRecordQuerySetTestCase(TestCase):
    def setUp(self):
        start_time = strftime("%H:%M")
        date = datetime.date(2022, 12, 19)
        self.user = User.objects.create(username="test")
        self.user_2 = User.objects.create(username="test_2")

        self.timer_first_user = TimeRecord.objects.create(
            user=self.user, date=date, start_time=start_time
        )
        self.timer_second_user = TimeRecord.objects.create(
            date=date, start_time=start_time, user=self.user_2
        )
        self.timer_end_time_first_user = TimeRecord.objects.create(
            user=self.user,
            date=date,
            start_time=start_time,
            end_time=timezone.now().time(),
        )
        self.timer_end_time_second_user = TimeRecord.objects.create(
            user=self.user_2,
            date=date,
            start_time=start_time,
            end_time=timezone.now().time(),
        )

    def test_filter_running_timers_ok(self):

        result = list(TimeRecord.objects.filter_running_timers())
        expected = [self.timer_first_user, self.timer_second_user]

        self.assertListEqual(result, expected)

    def test_filter_running_timers_of_user(self):
        result = list(TimeRecord.objects.filter_running_timers(user=self.user))
        expected = [self.timer_first_user]

        self.assertListEqual(result, expected)
