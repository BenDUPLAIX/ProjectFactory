from django.contrib import admin
from django.urls import path, include
from FRONT_OFFICE.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("front/", include("FRONT_OFFICE.urls")),
    path("back/", include("BACK_OFFICE.urls")),
    path("", home, name="home"),  # ✅ Page d'accueil
]