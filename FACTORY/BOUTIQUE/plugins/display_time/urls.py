from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="display_time_index"),
]
