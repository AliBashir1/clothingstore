from django.urls import path, include, re_path
from .views import (ProductHome, ProcessForm,
                    TestForms, TestClass,
                    ProductDetail, ProductUpdate,
                    InventoryForm )

#
urlpatterns = [

    path('', ProductHome.as_view(), name='product-home'),
    path('process_form/', ProcessForm.as_view(), name='process-form'),
    path('product_detail/<product_type>/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product_detail/<product_type>/<int:pk>/update', ProductUpdate.as_view(), name='product-update'),
    # Inventory view will be use for update or creating first time instance
    path('inventory_detail/<product_type>/<int:pk>/inventory', InventoryForm.as_view(), name='inventory-form'),

    # test views
    path('test/', TestClass.as_view(), name='test'),
    path('testform/', TestForms.as_view(), name='testform'),



]