from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from importlib import import_module
from FRONT_OFFICE.views import home
from BACK_OFFICE.models import Plugin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("front/", include("FRONT_OFFICE.urls")),
    path("back/", include("BACK_OFFICE.urls")),
    path("", home, name="home"),  # ✅ Page d'accueil
    path("login/", auth_views.LoginView.as_view(template_name="user_management/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

]

# Inclure dynamiquement les URLs des plugins activés
for plugin in Plugin.objects.filter(enabled=True):
    try:
        app_name = f"plugins.{plugin.name}"
        plugin_urls = import_module(f"{app_name}.urls")
        urlpatterns.append(path(f"plugins/{plugin.name}/", include(plugin_urls)))
        print(f"Plugin {plugin.name} chargé avec succès.")
    except ImportError as e:
        print(f"Erreur lors du chargement des URLs du plugin '{plugin.name}': {e}")