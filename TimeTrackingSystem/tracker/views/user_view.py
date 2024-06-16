from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tracker.views.access_views import role_required
from tracker.models.User import User
from tracker.forms import UserAddForm, UserEditForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()

@login_required
@role_required('manager')
def create_user(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            role_name = form.cleaned_data.get('role')
            create_user_role(user, role_name)
            return redirect('user_list')
    else:
        form = UserAddForm()
    return render(request, 'tracker/user/add_user.html', {'form': form})

def create_user_role(user, role_name):
    group, created = Group.objects.get_or_create(name=role_name)
    if group:
        user.groups.add(group)
        user.save()

@login_required
@role_required('manager')
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            role_name = form.cleaned_data.get('role')
            update_user_role(user, role_name)
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'tracker/user/edit_user.html', {'form': form, 'user': user})

def update_user_role(user, role_name):
    group, created = Group.objects.get_or_create(name=role_name)
    if group:
        user.groups.clear()
        user.groups.add(group)
        user.save()

@login_required
@role_required('manager')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')

@login_required
@role_required('manager')
def user_list(request):
    users = User.objects.all()
    return render(request, 'tracker/user/user_list.html', {'users': users})
