from django.urls import path
from .views import manage_users, signup, edit_user, forbidden, manage_plugins, upload_plugin, plugin_disabled


urlpatterns = [
    path("users/", manage_users, name="manage_users"),
    path("users/edit/<int:user_id>/", edit_user, name="edit_user"),
    path("signup/", signup, name="signup"),  # ✅ Page d'inscription
    path("forbidden/", forbidden, name="forbidden"),
    path("plugins/manage/", manage_plugins, name="manage_plugins"),
    path("plugins/upload/", upload_plugin, name="upload_plugin"),
    path("plugin-disabled/", plugin_disabled, name="plugin_disabled"),
]

