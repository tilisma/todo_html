from django.contrib import admin
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user',)
    list_filter = ('user',)
admin.site.register(UserProfile, UserProfileAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_date', 'created_by',)
    list_filter = ('created_by',)
admin.site.register(Task, TaskAdmin)
