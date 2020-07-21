from .models import Shoes, Accessories, Tops, Bottoms, Suppliers, Inventory
from django import forms
# from betterforms.multiform import MultiModelForm
# https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/

class ProductAddForm:
    model_mapping = {
        'Tops': Tops,
        'Bottoms': Bottoms,
        'Accessories': Accessories,
        'Shoes': Shoes,
        'Suppliers': Suppliers
    }

    def __init__(self, model, instance=None):
        self.model = self.model_mapping.get(model)

        class CreateForm(forms.ModelForm):
            class Meta:
                model = self.model
                fields = '__all__'
                exclude = ['slug']
        # return pre populated  form to be used in update view
        if instance is None:
            self.form_class = CreateForm
        else:
            self.form_class = CreateForm(instance=instance)


class InventoryAddForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ['product_id', 'product_cost', 'product_count']

class TopsAddForm(forms.ModelForm):

    class Meta:
        model = Tops
        fields = '__all__'
        exclude = ['slug']
