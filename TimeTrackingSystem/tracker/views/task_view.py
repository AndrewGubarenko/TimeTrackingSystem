from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tracker.views.access_views import role_required
from tracker.models.Project import Project
from tracker.models.Task import Task
from tracker.models.TimeLog import TimeLog
from tracker.models.Comment import Comment
from tracker.forms import TaskForm, CommentFormSet


@login_required
@role_required('manager', 'developer')
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = Comment.objects.filter(task=task)
    time_logs = TimeLog.objects.filter(task=task)
    
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        comment_formset = CommentFormSet(request.POST, instance=task)
        if task_form.is_valid() and comment_formset.is_valid():
            task_form.save()
            comment_formset.save()
    else:
        task_form = TaskForm(instance=task)
        comment_formset = CommentFormSet(instance=task)
    
    return render(request, 'tracker/task/task_detail.html', {
        'project_slug': task.project.slug,
        'task_form': task_form,
        'comment_formset': comment_formset,
        'task': task,
        'comments': comments,
        'time_logs': time_logs
    })

@login_required
@role_required('manager')
def add_task(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False, project=project, author=request.user)
            task.save()
            return redirect('project_detail', slug=project.slug)
    else:
        form = TaskForm(initial={'author': request.user})
    return render(request, 'tracker/task/add_task.html', {'form': form, 'project': project})

@login_required
@role_required('manager')
def edit_task(request, slug, task_id):
    project = get_object_or_404(Project, slug=slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tracker/task/edit_task.html', {
        'form': form, 
        'project': project, 
        'task': task})

@login_required
@role_required('manager')
def delete_task(request, slug, task_id):
    project = get_object_or_404(Project, slug=slug)
    task = get_object_or_404(Task, id=task_id, project=project)
    
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', slug=project.slug)
    
    return redirect('task_detail', task_id=task_id)
