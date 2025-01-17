from django.shortcuts import redirect
from .models import Plugin

def plugin_enabled(plugin_name):
    """
    Décorateur pour vérifier si un plugin est activé.
    Redirige vers une page par défaut si le plugin n'est pas activé.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                plugin = Plugin.objects.get(name=plugin_name)
                if plugin.enabled:
                    return view_func(request, *args, **kwargs)
            except Plugin.DoesNotExist:
                pass
            # Redirige vers une page par défaut si le plugin n'est pas activé
            return redirect("plugin_disabled")
        return _wrapped_view
    return decorator
