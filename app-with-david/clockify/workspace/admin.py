from django.contrib import admin
from .models import (
    Project,
    Currency,
    Task,
    TimeRecord,
    Report,
    User,
    Role,
    UserProject,
    UserTask,
)

# Register your models here.


class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ["id", "start_time", "end_time", "date"]


myModels = [Project, Currency, Task, Report, User, Role, UserProject, UserTask]
admin.site.register(myModels)
admin.site.register(TimeRecord, TimeRecordAdmin)
