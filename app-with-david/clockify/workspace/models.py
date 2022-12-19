from datetime import datetime
from time import strftime, gmtime
from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Optional
from time import gmtime, strftime
from django.utils import timezone

from workspace.querysets import TimeRecordQuerySet

# Create your models here.


class Currency(models.Model):
    shortcut_name = models.CharField(max_length=3)

    def __str__(self):
        return self.shortcut_name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    hex_color = models.CharField(max_length=7)  # predefined colors + color picker
    hourly_rate = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_allocated_hours = models.FloatField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TimeRecord(models.Model):
    description = models.TextField(max_length=1024, null=True, blank=True)
    start_time = (
        models.TimeField()
    )  # auto add time when Object is created, make it editable
    end_time = models.TimeField(null=True, blank=True)
    date = models.DateField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="time_records"
    )

    objects = TimeRecordQuerySet.as_manager()

    def __str__(self):
        if self.task:
            return f"{self.task} - {self.start_time}"
        return f"{self.id} - {self.start_time}"

    # def save(self, *args, **kwargs):
    #     # todo allow only one running instance
    #     # find all running instances
    #     # kill them

    #     super().save(*args, **kwargs)

    #     running_records = self.objects.filter_running_timers(self.user)
    #     if running_records.count() > 1:
    #         last_record = running_records.latest("id")
    #         all_other_records = self.objects.exclude(pk__in=list(last_record))
    #         self.stop_time(all_other_records)

    def change_start_time(self, start_time):
        self.start_time = start_time
        self.save()

    # todo
    def stop_time(self):
        # check if after midnight
        start_time = datetime.strptime(self.start_time.replace(":", ""), "%H%M")  # 1000
        # todo dont use gmtime
        end_time = strftime("%H:%M", gmtime())
        now = datetime.now()

        if self.date == now.date():
            self.end_time = end_time
            self.save()
            return

        self.end_time = "23:59"
        # todo create new time record when over midnight
        return self.save()


class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class User(AbstractUser):
    def __str__(self):
        return self.email

    def get_currently_running_timer(self) -> TimeRecord:
        """If nothing found in queryset throws TimeRecord.DoesNotExist"""
        time_records = self.time_records.filter(end_time__isnull=True)

        if time_records.count() > 1:
            # throw error/ kill all but last
            last_record = time_records.latest("id")
            all_other_records = time_records.exclude(pk__in=list(last_record))
            self.stop_time(all_other_records)
            return last_record.get()

        return time_records.get()


class Role(models.Model):
    name = models.CharField(max_length=8)
    description = models.TextField()
    permissions = models.ManyToManyField("Permission", related_name="roles")

    def __str__(self):
        return self.name


class Permission(models.Model):
    PERMISSION_CHOICES = [
        ("add_project", "add_project"),
        ("edit_prject", "edit_project"),
        ("delete_project", "delete_project"),
        ("add_task", "add_task"),
        ("edit_task", "edit_task"),
        ("delete_task", "delete_task"),
        ("add_time_record", "add_time_record"),
        ("edit_time_record", "edit_time_record"),
        ("delete_time_record", "delete_time_record"),
        ("view", "view"),
        ("generate_report", "generate_report"),
    ]
    name = models.CharField(max_length=20, choices=PERMISSION_CHOICES)


class UserTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)


class UserProjects(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
