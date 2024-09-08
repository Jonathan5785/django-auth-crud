from django.urls import path
from . import views

tasks_patterns = ([
    path("", views.HomePageView.as_view(), name="home"),
    path("signup/", views.signup, name="signup"),
    path("tasks/pending", views.TaskPendingListView.as_view(), name="tasks_pending"),
    path("tasks/completed", views.TaskCompletedListView.as_view(), name="tasks_completed"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="create_task"),
    path("tasks/task_detail/<int:pk>", views.TaskUpdateView.as_view(), name="task_detail"),
    path("tasks/task_detail/<int:pk>/complete", views.TaskCompleteView.as_view(), name="complete_task"),
    path("tasks/task_detail/<int:pk>/delete", views.TaskDeleteView.as_view(), name="delete_task"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # path("signin/", views.signin, name="signin"),
    path("signin/", views.LoginView.as_view(), name="signin"),
],'tasks')