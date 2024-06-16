from django import forms
from django.forms import inlineformset_factory, DateInput
from tracker.models.User import User
from tracker.models.Project import Project
from tracker.models.Task import Task
from tracker.models.TimeLog import TimeLog
from tracker.models.Comment import Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'slug']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'end_date', 'task_type', 'priority', 'estimated_hours', 'executor']
        widgets = {
            'start_date': DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
            'end_date': DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True, project=None, author=None):
        instance = super().save(commit=False)
        if project:
            instance.project = project
        if author:
            instance.author = author
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

CommentFormSet = inlineformset_factory(Task, Comment, form=CommentForm, extra=1)

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['hours_spent', 'comment', 'task']
        widgets = {
            'task': forms.HiddenInput()
        }

User = get_user_model()

class UserAddForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'birth_date',
            'position', 'avatar', 'password1', 'password2', 'role', 'avatar'
        ]
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }

class UserEditForm(UserChangeForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'birth_date',
            'position', 'avatar', 'role', 'avatar'
        ]
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }
        