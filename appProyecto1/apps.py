from django.apps import AppConfig

class Appproyecto1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appProyecto1'

    def ready(self):
        import appProyecto1.signals
