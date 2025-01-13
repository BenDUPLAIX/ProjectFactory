from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, get_user_model
from .forms import SignUpForm, UserEditForm
from .models import CustomUser as User

User = get_user_model()


# Vérifie si l'utilisateur est admin
def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)  # ✅ Seuls les super-utilisateurs peuvent voir cette page
def manage_users(request):
    users = User.objects.all()
    return render(request, "back_office/manage_users.html", {"users": users})


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

    return render(request, "back_office/edit_user.html", {"form": form, "user": user})

@login_required
def manage_users(request):
    return render(request, "user_management/manage_users.html")


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