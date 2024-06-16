from django.contrib import admin
from tracker.models.User import User
from tracker.models.Project import Project
from tracker.models.Task import Task
from tracker.models.TimeLog import TimeLog
from tracker.models.Comment import Comment


admin.site.register(Project)
admin.site.register(User)
admin.site.register(Task)
admin.site.register(TimeLog)
admin.site.register(Comment)
