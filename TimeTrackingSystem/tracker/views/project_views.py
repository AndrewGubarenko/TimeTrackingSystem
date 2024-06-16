from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tracker.views.access_views import role_required
from tracker.models.Project import Project
from tracker.forms import ProjectForm


@login_required
@role_required('manager', 'developer')
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/project/project_list.html', {'projects': projects})

@login_required
@role_required('manager', 'developer')
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    tasks = project.task_set.all()
    return render(request, 'tracker/project/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
@role_required('manager')
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    return render(request, 'tracker/project/create_project.html', {'form': form})

@login_required
@role_required('manager')
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'tracker/project/edit_project.html', {'form': form, 'project': project})

@login_required
@role_required('manager')
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    
    return redirect('projects', slug=slug)
