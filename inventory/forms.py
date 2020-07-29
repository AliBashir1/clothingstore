from .models import Shoes, Accessories, Tops, Bottoms, Suppliers, Inventory
from django import forms
# from betterforms.multiform import MultiModelForm
# https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/

#
# class ProductAddForm:
#     model_mapping = {
#         'Tops': Tops,
#         'Bottoms': Bottoms,
#         'Accessories': Accessories,
#         'Shoes': Shoes,
#         'Suppliers': Suppliers,
#     }
#     model = None
#     fields = None
#     exclude =None
#
#     def __init__(self, model, instance=None):
#         self.model = self.model_mapping.get(model)
#
#         class CreateForm(forms.ModelForm):
#             class Meta:
#                 model = self.model
#                 fields = '__all__'
#                 exclude = ['slug']
#         # return pre populated  form to be used in update view
#         if instance is None:
#             self.form_class = CreateForm
#         else:
#             self.form_class = CreateForm(instance=instance)


class GetForm:

    model_mapping = {
        'Tops': Tops,
        'Bottoms': Bottoms,
        'Accessories': Accessories,
        'Shoes': Shoes,
        'Suppliers': Suppliers,
        'Inventory': Inventory
    }

    _model = None
    _fields = None
    _exclude = ['slug']

    def __init__(self, product_type, instance=None):
        self._model = self.model_mapping.get(product_type)

        if product_type == 'Inventory':
            self._fields = ['product_cost', 'product_count']
        else:
            self._fields = '__all__'

        class CreateForm(forms.ModelForm):

            class Meta:
                model = self._model
                fields = self._fields
                exclude = self._exclude

        if instance is None:
            print("instance is None True : {}".format(instance))
            self.form_class = CreateForm
        else:
            print("instance is None False : {}".format(instance))
            self.form_class = CreateForm(instance=instance)



