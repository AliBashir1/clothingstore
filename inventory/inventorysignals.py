# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from .models import Inventory, Tops, Bottoms, Accessories,Shoes
# from datetime import datetime
# from django.contrib.contenttypes.models import ContentType
#
#
# @receiver(post_save, sender=Tops)
# @receiver(post_save, sender=Bottoms)
# @receiver(post_save, sender=Accessories)
# @receiver(post_save, sender=Shoes)
# def add_inventory(sender, instance, created, **kwargs):
#     """
#
#     :param sender (Model):
#     :param instance(object of Model):
#     :param created (boolean):
#     :param kwargs:
#     :return:
#     """
#
#     # inventory_count = Inventory.objects.
#     # todo debug purpose delete this
#     print("instance: {} \nsender: {}\ncreated: {}\nkwargs: {}".format(instance, sender, created, kwargs))
#
#     instanceClassname = ContentType.objects.get(model__iexact=instance.get_classname())
#
#     if created:
#         Inventory.objects.create(product_id=instance.product_id,
#                                  # product_count=instance.product_count,
#                                  # product_cost=instance.product_cost,
#                                  added_at=datetime.now(),
#                                  updated_at=datetime.now(),
#                                  content_type_id=instanceClassname.pk)
#         # print("product {} added in inventory ".format(instance.product_id))
#
#
#
#
#
#
#
#
#
