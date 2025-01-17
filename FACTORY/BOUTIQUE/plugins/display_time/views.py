from django.shortcuts import render
from datetime import datetime
from BACK_OFFICE.decorators import plugin_enabled

@plugin_enabled("display_time")  # Vérifie si le plugin est activé
def index(request):
    """
    Vue principale du plugin display_time.
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    return render(request, "display_time/templates/index.html", {"current_time": current_time})
