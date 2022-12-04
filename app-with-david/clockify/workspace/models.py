from django.db import models
from django.contrib.auth.models import AbstractUser

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
	hex_color =  models.CharField(max_length=7) # predefined colors + color picker
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
	start_time = models.TimeField() # auto add time when Object is created, make it editable
	end_time = models.TimeField(null=True, blank=True)
	date = models.DateField()
	task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="time_records")

	objects = TimeRecordQuerySet.as_manager()

	def __str__(self):
		if self.task:
			return f"{self.task} - {self.start_time}"
		return  f"{self.id} - {self.start_time}"

	def change_start_time(self, start_time):
		self.start_time = start_time
		self.save()

class Report(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)

class User(AbstractUser):
	pass
	def __str__(self):
			return self.email

class Role(models.Model):
	name = models.CharField(max_length=8)
	description = models.TextField()
	permissions = models.ManyToManyField("Permission", related_name="roles")
  
	def __str__(self):
		return self.name

class Permission(models.Model):
	PERMISSION_CHOICES = [
		('add_project', 'add_project'),
		('edit_prject', 'edit_project'),
		('delete_project', 'delete_project'),
		('add_task', 'add_task'),
		('edit_task', 'edit_task'),
		('delete_task', 'delete_task'),
		('add_time_record', 'add_time_record'),
		('edit_time_record', 'edit_time_record'),
		('delete_time_record', 'delete_time_record'),
		('view', 'view'),
		('generate_report', 'generate_report')
	]
	name = models.CharField(max_length=20, choices=PERMISSION_CHOICES)

class UserTasks(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	task = models.ForeignKey(Task, on_delete=models.PROTECT)

class UserProjects(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	project = models.ForeignKey(Project, on_delete=models.PROTECT)
