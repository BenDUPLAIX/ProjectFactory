from importlib import import_module

def load_plugin_views(plugin_name):
    """
    Charge les vues d'un plugin dynamiquement.
    """
    try:
        views = import_module(f"plugins.{plugin_name}.views")
        print(f"Vues du plugin '{plugin_name}' chargées avec succès.")
        return views
    except ImportError as e:
        print(f"Erreur lors du chargement des vues du plugin '{plugin_name}': {e}")
        return None
