from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from functools import wraps
from tracker.forms import LoginForm

# Create your views here.

def role_required(*role_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                for role_name in role_names:
                    if request.user.groups.filter(name=role_name).exists():
                        return view_func(request, *args, **kwargs)
            return access_denied(request)
        return _wrapped_view
    return decorator

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('projects/')
            else:
                form.add_error(None, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def access_denied(request):
    return render(request, 'tracker/access_denied.html')
