from django.shortcuts import render, get_object_or_404, redirect
from tracker.models.Task import Task
from tracker.models.Comment import Comment
from tracker.forms import CommentForm
from django.contrib.auth.decorators import login_required
from tracker.views.access_views import role_required
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required
@role_required('manager', 'developer')
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.task = task  
            new_comment.save()
            return redirect('task_detail', task_id=task.id)
    else:
        comment_form = CommentForm()

    return render(request, 'tracker/comment/add_comment.html', {
        'task': task,
        'comment_form': comment_form
    })


@login_required
@role_required('manager', 'developer')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=comment.task.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'tracker/comment/edit_comment.html', {
        'form': form,
        'task': comment.task,
        })

@login_required
@role_required('manager', 'developer')
def delete_comment(request, task_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.delete()
        return redirect('task_detail', task_id=task_id)
    
    return redirect('task_detail', task_id=task_id)
