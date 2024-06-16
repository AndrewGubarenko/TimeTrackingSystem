from django.db import models
from tracker.models.Project import Project
from tracker.models.User import User


class Task(models.Model):
    FEATURE = 'feature'
    BUG = 'bug'
    TASK_TYPES = [
        (FEATURE, 'Feature'),
        (BUG, 'Bug'),
    ]

    NORMAL = 'normal'
    HIGH = 'high'
    URGENT = 'urgent'
    PRIORITIES = [
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
        (URGENT, 'Urgent'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    task_type = models.CharField(max_length=10, choices=TASK_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITIES)
    estimated_hours = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='executed_tasks', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='authored_tasks', on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', related_name='related_tasks', blank=True)

    def __str__(self):
        return self.title
