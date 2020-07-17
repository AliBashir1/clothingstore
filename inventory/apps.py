from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        """
        This is important for signal to work properly - Please read
        https://docs.djangoproject.com/en/3.0/topics/signals/#defining-and-sending-signals
        :return:
        """
        import inventory.inventorysignals
