from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now  # Utiliser l'heure actuelle
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Plugin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    installed_at = models.DateTimeField(default=now)  # Utilise la date actuelle comme valeur par défaut

    def __str__(self):
        return f"{self.name} ({'Activé' if self.enabled else 'Désactivé'})"
