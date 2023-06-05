from django.contrib import admin
from .models import Tasks
# Register your models here.


class TasksAdmin(admin.ModelAdmin):
  list_display = ("username","desc","task","due_date","priority","completed","assigned_to")
  
admin.site.register(Tasks,TasksAdmin)