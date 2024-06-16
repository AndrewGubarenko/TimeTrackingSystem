from django.db import models
from tracker.models.Task import Task
from tracker.models.User import User


class TimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hours_spent = models.FloatField()
    comment = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hours_spent} hours on {self.task}'
