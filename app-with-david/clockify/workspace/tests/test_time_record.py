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


# Create your tests here.


class TimeRecordTestCase(TestCase):
    def setUp(self):  # runs before every test
        self.user = User.objects.create(username="test")

    def tearDown(self):  # runs after every test
        pass

    def test_stop_time_after_midnight(self):
        start_time = strftime("%H:%M")
        date = datetime.date(2022, 12, 19)
        timer = TimeRecord.objects.create(user=self.user, date=date, start_time=start_time)

        with patch("workspace.models.datetime") as datetime_mock:
            datetime_mock.now = Mock()
            datetime_mock.now.return_value = datetime.datetime(2023, 12, 19)

            timer.stop_time()

        self.assertEqual(timer.end_time, "23:59")
        self.assertEqual(TimeRecord.objects.all().count(), 2)

    # todo test_stop_time_same_day()
    def test_stop_time_same_day(self):
        start_time = strftime("%H:%M")
        now = datetime.datetime.now()
        date = now.date()
        timer = TimeRecord.objects.create(user=self.user, start_time=start_time, date=date)
        timer.stop_time()

        self.assertEqual(timer.date, date)
        self.assertEqual(timer.end_time, strftime("%H:%M"))


# user = User.objects.create(username="test7")
# start_time = strftime("%H:%M")
# now = datetime.datetime.now()
# today = now.date()
# stop_time = now
# timer = TimeRecord.objects.create(user=user, start_time=start_time, date=today)
# print(timer.now)
