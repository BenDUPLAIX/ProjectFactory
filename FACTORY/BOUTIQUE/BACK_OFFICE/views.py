import os
import zipfile
import shutil
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from .forms import SignUpForm, UserEditForm
from .models import CustomUser as User
from .models import Plugin


User = get_user_model()


# Vérifie si l'utilisateur est admin
def is_admin(user):
    return user.is_superuser

def forbidden(request):
    return render(request, "user_management/forbidden.html", {
        "message": "Vous n'êtes pas autorisé à accéder à cette page.",
        "next": request.GET.get("next", "/")  # Retourne à l'accueil par défaut
    })

@login_required
@user_passes_test(is_admin, login_url=reverse_lazy("forbidden"))  #
def manage_users(request):
    users = User.objects.all()
    print("Utilisateurs récupérés :", users)  # ✅ Ajout d'un print pour debug
    return render(request, "user_management/manage_users.html", {"users": users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("manage_users")
    else:
        form = UserEditForm(instance=user)

    return render(request, "user_management/edit_user.html", {"form": form, "user": user})



def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # ✅ On ne sauvegarde pas encore

            # ✅ Vérifier s'il y a déjà un super-utilisateur
            if not User.objects.filter(is_superuser=True).exists():
                user.is_superuser = True
                user.is_staff = True  # ✅ Donne aussi accès à l'admin

            user.save()  # ✅ Maintenant on sauvegarde avec les droits définis
            login(request, user)  # ✅ Connexion automatique après inscription
            return redirect("home")  # ✅ Redirige vers la page d'accueil
    else:
        form = SignUpForm()

    return render(request, "user_management/signup.html", {"form": form})


def manage_plugins(request):
    # Chemin des plugins
    plugins_path = os.path.join(settings.BASE_DIR, "plugins")
    os.makedirs(plugins_path, exist_ok=True)

    # Liste des dossiers dans "plugins/"
    plugin_dirs = [name for name in os.listdir(plugins_path) if os.path.isdir(os.path.join(plugins_path, name))]

    # Liste des plugins enregistrés dans la base
    registered_plugins = Plugin.objects.values_list("name", flat=True)

    # Identifier l'état des plugins
    plugins_status = []
    for plugin_name in plugin_dirs:
        is_installed = plugin_name in registered_plugins
        if is_installed:
            plugin = Plugin.objects.get(name=plugin_name)
            is_enabled = plugin.enabled
        else:
            is_enabled = False

        plugins_status.append({
            "name": plugin_name,
            "is_installed": is_installed,
            "is_enabled": is_enabled,
        })

    # Gérer les actions (installer, désinstaller, supprimer, activer/désactiver)
    if request.method == "POST":
        action = request.POST.get("action")
        plugin_name = request.POST.get("plugin_name")

        if action == "install" and plugin_name in plugin_dirs:
            if not Plugin.objects.filter(name=plugin_name).exists():
                Plugin.objects.create(
                    name=plugin_name,
                    enabled=False,
                    description=f"Plugin {plugin_name} détecté automatiquement."
                )
            return redirect("manage_plugins")

        elif action == "uninstall" and plugin_name in registered_plugins:
            Plugin.objects.filter(name=plugin_name).delete()
            return redirect("manage_plugins")

        elif action == "delete" and plugin_name in plugin_dirs:
            plugin_dir = os.path.join(plugins_path, plugin_name)
            shutil.rmtree(plugin_dir)
            return redirect("manage_plugins")

        elif action == "toggle" and plugin_name in registered_plugins:
            plugin = Plugin.objects.get(name=plugin_name)
            plugin.enabled = not plugin.enabled
            plugin.save()
            return redirect("manage_plugins")

    return render(request, "plugin_management/manage_plugins.html", {
        "plugins_status": plugins_status,
    })


def upload_plugin(request):
    plugins_path = os.path.join(settings.BASE_DIR, "plugins")

    if request.method == "POST" and request.FILES["plugin_file"]:
        plugin_file = request.FILES["plugin_file"]
        plugin_name = os.path.splitext(plugin_file.name)[0]

        # Chemin où le plugin sera décompressé
        plugin_dir = os.path.join(plugins_path, plugin_name)

        # Créer le dossier si nécessaire
        os.makedirs(plugins_path, exist_ok=True)

        # Sauvegarder le fichier ZIP
        zip_path = os.path.join(plugins_path, plugin_file.name)
        with open(zip_path, "wb") as f:
            for chunk in plugin_file.chunks():
                f.write(chunk)

        # Décompresser le fichier ZIP
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(plugin_dir)

        # Supprimer le fichier ZIP après extraction
        os.remove(zip_path)

        # Ajouter le plugin à la base de données si ce n'est pas déjà fait
        if not Plugin.objects.filter(name=plugin_name).exists():
            Plugin.objects.create(
                name=plugin_name, enabled=False, description=f"Plugin {plugin_name} ajouté."
            )

        return redirect("manage_plugins")

    return render(request, "plugin_management/upload_plugin.html")

def plugin_disabled(request):
    """
    Vue pour afficher une page par défaut lorsque le plugin est désactivé.
    """
    return render(request, "plugin_management/plugin_disabled.html")