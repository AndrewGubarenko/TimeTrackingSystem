from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tracker.forms import TimeLogForm
from tracker.models.Task import Task
from tracker.models.TimeLog import TimeLog
from tracker.views.access_views import role_required


@login_required
@role_required('manager', 'developer')
def add_time_log(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TimeLogForm(request.POST)
        if form.is_valid():
            time_log = form.save(commit=False)
            time_log.user = request.user
            time_log.task = task
            time_log.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TimeLogForm(initial={'task': task})
        
    return render(request, 'tracker/time_log/add_time_log.html', {'form': form, 'task': task})

@login_required
@role_required('manager', 'developer')
def edit_time_log(request, task_id, log_id):
    task = get_object_or_404(Task, id=task_id)
    time_log = get_object_or_404(TimeLog, id=log_id, task=task)

    if request.method == 'POST':
        form = TimeLogForm(request.POST, instance=time_log)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TimeLogForm(instance=time_log)

    return render(request, 'tracker/time_log/edit_time_log.html', {'form': form, 'task': task})

@login_required
@role_required('manager', 'developer')
def delete_time_log(request, task_id, log_id):
    task = get_object_or_404(Task, id=task_id)
    time_log = get_object_or_404(TimeLog, id=log_id, task=task)
    
    if request.method == 'POST':
        time_log.delete()
        return redirect('task_detail', task_id=task.id)

    return redirect('task_detail', task_id=task.id)
