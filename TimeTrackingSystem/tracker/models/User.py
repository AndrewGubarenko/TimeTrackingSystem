from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MANAGER = 'manager'
    DEVELOPER = 'developer'
    ROLE_CHOICES = [
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    groups = models.ManyToManyField('auth.Group', related_name='tracker_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='tracker_user_permissions')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_role_display(self):
        group = self.groups.first()
        if group:
            return next((role_display for role, role_display in self.ROLE_CHOICES if role == group.name), "Unknown Role")
        return "Unknown Role"
