from django.contrib import admin
from .models import (Suppliers, Shoes, Accessories, Tops, Bottoms, Inventory)

# Register your models here.

admin.site.register(Suppliers)
admin.site.register(Shoes)
admin.site.register(Accessories)
admin.site.register(Tops)
admin.site.register(Bottoms)
admin.site.register(Inventory)