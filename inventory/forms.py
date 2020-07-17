from .models import Shoes, Accessories, Tops, Bottoms, Suppliers, Inventory
from django import forms


class ProductAddForm:
    model_set = {
        'Tops': Tops,
        'Bottoms': Bottoms,
        'Accessories': Accessories,
        'Shoes': Shoes,
        'Suppliers': Suppliers
    }

    def __init__(self, model, instance=None):
        self.model = self.model_set.get(model)

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
        fields = ['product_cost', 'product_count']
