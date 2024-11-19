from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("signup/", views.signup_view, name='signup'),
    path("todo/", views.todo_view, name='todo'),
    path("delete/<int:id>", views.delete_todo_view, name='delete-todo'),
    path("edit/<slug:id>", views.toggle_completed_view, name='edit-todo'),
]