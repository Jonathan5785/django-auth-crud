from django.urls import path,include
from . import views
from django.views.generic.base import RedirectView

tasks_patterns = ((
    path("pending/", views.TaskPendingListView.as_view(), name="tasks_pending"),
    path("completed/", views.TaskCompletedListView.as_view(), name="tasks_completed"),
    path("create/", views.TaskCreateView.as_view(), name="create_task"),
    path("task_detail/<int:pk>", views.TaskUpdateView.as_view(), name="task_detail"),
    path("task_detail/<int:pk>/complete", views.TaskCompleteView.as_view(), name="complete_task"),
    path("task_detail/<int:pk>/delete", views.TaskDeleteView.as_view(), name="delete_task"),
),'tasks',)

user_patterns = ((
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("list/",views.UserListView.as_view(),name='list'),
    path("<int:user_id>/update/",views.UserUpdateView.as_view(),name='update'),
    
),'user',)


app_name = "web"
urlpatterns = (
    path("",RedirectView.as_view(pattern_name="web:home")),
    path("home/", views.HomePageView.as_view(), name="home"),
    path("signin/", views.LoginView.as_view(), name="signin"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password-change/", views.PasswordChangeView.as_view(), name="password-change"),
    path("tasks/",include(tasks_patterns)),
    path("user/",include(user_patterns))
)