from django.urls import path
from .views import manage_users, signup, edit_user

urlpatterns = [
    path("users/", manage_users, name="manage_users"),
    path("users/edit/<int:user_id>/", edit_user, name="edit_user"),
    path("signup/", signup, name="signup"),  # ✅ Page d'inscription

]