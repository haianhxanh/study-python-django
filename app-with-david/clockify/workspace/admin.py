from django.contrib import admin
from .models import Project, Currency, Task, TimeRecord, Report, User, Role
# Register your models here.

myModels = [Project, Currency, Task, TimeRecord, Report, User, Role] 
admin.site.register(myModels)
