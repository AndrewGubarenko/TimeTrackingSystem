from django.urls import path
from django.contrib.auth.views import LoginView
from tracker.views import log_views, project_views, task_view, comment_view, user_view


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  
    
    #logs
    path('tasks/<int:task_id>/add_time_log/', log_views.add_time_log, name='add_time_log'),
    path('tasks/<int:task_id>/edit_time_log/<int:log_id>/', log_views.edit_time_log, name='edit_time_log'),
    path('tasks/<int:task_id>/delete_time_log/<int:log_id>/', log_views.delete_time_log, name='delete_time_log'),
    
    #task
    path('tasks/<int:task_id>/', task_view.task_detail, name='task_detail'),
    path('projects/<slug:slug>/add_task/', task_view.add_task, name='add_task'),
    path('edit_tasks/<slug:slug>/<int:task_id>/', task_view.edit_task, name='edit_task'),
    path('delete_tasks/<slug:slug>/<int:task_id>/', task_view.delete_task, name='delete_task'),
   
    #projects
    path('projects/', project_views.project_list, name='project_list'),
    path('projects/<slug:slug>/', project_views.project_detail, name='project_detail'),
    path('create_project/', project_views.add_project, name='create_project'),
    path('edit_project/<slug:slug>/', project_views.edit_project, name='edit_project'),
    path('delete_project/<slug:slug>/', project_views.delete_project, name='delete_project'),
    
    #comments
    path('tasks/<int:task_id>/add_comment/', comment_view.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', comment_view.edit_comment, name='edit_comment'),
    path('tasks/<int:task_id>/delete_comment/<int:comment_id>/', comment_view.delete_comment, name='delete_comment'),

    #user
    path('users/', user_view.user_list, name='user_list'),
    path('users/create/', user_view.create_user, name='create_user'),
    path('users/<int:user_id>/edit/', user_view.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', user_view.delete_user, name='delete_user'),
]
    