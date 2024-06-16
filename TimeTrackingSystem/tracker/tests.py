from django.test import TestCase
from tracker.models.User import User
from tracker.models.Project import Project
from tracker.models.Task import Task
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create your tests here.

# model tests
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            slug='slu'
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test Description')
        self.assertEqual(self.project.slug, 'slu')

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            slug='slu'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
            task_type='Bug',
            priority='Urgent',
            estimated_hours=4,
            executor=self.user,
            project=self.project,
            author=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Task Description')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.author, self.user)


# views test

User = get_user_model()

class ProjectViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            password='password',
            email='test@example.com'
        )
        group, created = Group.objects.get_or_create(name='manager')
        self.user.groups.add(group)
        self.user.user_permissions.add(27)
        
        self.client.login(username='testuser2', password='password')

        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            slug='slu'
        )

    def test_project_list_view(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_project_detail_view(self):
        response = self.client.get(reverse('project_detail', args=[self.project.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Test Description')
