from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_habit, name="add"),
    path("<int:pk>/", views.habit_detail, name="detail"),
    path("<int:pk>/edit/", views.edit_habit, name="edit"),
    path("<int:pk>/delete/", views.delete_habit, name="delete"),
    path("<int:pk>/analytics/", views.analytics, name="analytics"),
    path("analytics/", views.analytics_overall, name="analytics_overall"),

]
