from django.apps import AppConfig


class BuyusaappConfig(AppConfig):
    name = 'buyusaapp'

    def ready(self):
        import buyusaapp.signals
