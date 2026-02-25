from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = 'services'
    
    def ready(self):
        """Register signal handlers when app is ready"""
        import services.signals  # noqa
