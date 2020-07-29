from django.urls import path, include, re_path
from .views import (ProductHome, ProcessForm,
                    ProductDetail, ProductUpdate)

#
urlpatterns = [

    path('', ProductHome.as_view(), name='product-home'),
    path('product_detail/<product_type>/<slug:slug>', ProductDetail.as_view(), name='product-detail'),

    # Process form urls
    path('process_form/', ProcessForm.as_view(), name='process-form'),
    path('product_detail/<product_type>/<inventory>/<slug:slug>', ProcessForm.as_view(), name='process-inventory-form'),

    # Update forms urls
    path('product_detail/<product_type>/update/<slug:slug>', ProductUpdate.as_view(), name='product-update'),
    # path('product_detail/<product_type>/update/<inventory>/<slug:slug>', ProductUpdate.as_view(), name='product-inventory-update')

    # Inventory view will be use for update or creating first time instance
    # path('product_detail/<product_type>/<slug:slug>/inventory', InventoryForm.as_view(), name='inventory-form'),



]

"""
update form is not working
"""