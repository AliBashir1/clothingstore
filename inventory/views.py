from django.shortcuts import render, reverse, get_object_or_404
from django.urls import path, re_path, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView, UpdateView
from .models import Shoes, Tops, Bottoms, Accessories, Suppliers, Inventory
from django.views.generic.edit import FormMixin
from .forms import  InventoryAddForm, ProductAddForm
from datetime import datetime
from django.contrib.contenttypes.models import ContentType


class ProductDetail(DetailView):
    models_mapping = {
        'Tops': Tops,
        'Bottoms': Bottoms,
        'Accessories': Accessories,
        'Shoes': Shoes,
        'Suppliers': Suppliers
    }
    context_object_name = 'product'
    template_name = 'inventory/product_details.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        product_type = self.kwargs.get('product_type')
        model = self.models_mapping.get(product_type)
        return get_object_or_404(klass=model, product_id=id)


#
class ProductUpdate(UpdateView):
    models_mapping = {
        'Tops': Tops,
        'Bottoms': Bottoms,
        'Accessories': Accessories,
        'Shoes': Shoes,
        'Suppliers': Suppliers
    }
    context_object_name = 'form'
    template_name = 'inventory/process_form.html'
    success_url = reverse_lazy('product-detail')

    def get_success_url(self):
        id = self.kwargs.get('pk')
        return reverse_lazy('product-detail', kwargs={'pk': id})

    def get_form_class(self, instance=None):
        """This method gets the product type from url which has similar name as model of product.
        That information is being used to get form_class from ProductAddForm.

        :param (Model) instance:
       :return (ModelForm) form_class:
        """
        product_type = self.kwargs.get('product_type')
        forms_obj = ProductAddForm(product_type, instance=instance)
        # Returns form_class from ProductAddForm
        return forms_obj.form_class

    def get_object(self, queryset=None):
        """Method uses pk(product_id) and product_type from url to get Model and object primary key
        which is used to return current instance.
        :param queryset:
        :return (MODEL) Object:
        """
        id = self.kwargs.get('pk')
        product_type = self.kwargs.get('product_type')
        model = self.models_mapping.get(product_type)
        return get_object_or_404(klass=model, product_id=id)

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['product_form'] = self.get_form_class(instance=obj)

        # only Products need inventory detail - find a better way to deal with this
        if self.kwargs.get('product_type') != 'Suppliers':
            inv_obj = Inventory.objects.get(content_type__model=obj.get_classname(), product_id=obj.product_id)
            context['inventory_form'] = InventoryAddForm(instance=inv_obj)
        return context

    def form_valid(self, form):
        """
         overriding form_valid to add inventory of product
        :param form:
        :return:
        """
        obj = form.save(commit=False)
        print(form.cleaned_data)
        # obj.inventory.product_count = form.cleaned_data[]
        # obj.inventory.product_cost= form.cleaned_data['product_cost']
        obj.save()
        # model = ContentType.objects.get(model__iexact=obj.get_classname())
        # Inventory.objects.create(product_id=obj.product_id,
        #                          product_count=self.request.POST.get('product_count'),
        #                          product_cost=self.request.POST.get('product_cost'),
        #                          # Date format 2014-07-05 14:34:14
        #                          updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        #                          content_type_id=model.pk)

        return super(ProductUpdate, self).form_valid(form)


# may be use list view for pagination

class ProductHome(TemplateView):

    # todo use this for list view of products

    # template_name = 'inventory/products_home.html'

    def get_template_names(self):
        # todo for future use this to get templates for admin vs regular user .
        if self.request:
            template_name = 'inventory/products_home.html'
            return template_name

    def get_context_data(self, **kwargs):
        context = super(ProductHome, self).get_context_data(**kwargs)
        context['shoes'] = Shoes.objects.all()
        context['bottoms'] = Bottoms.objects.all()
        context['accessories'] = Accessories.objects.all()
        context['tops'] = Tops.objects.all()

        return context


# Dynamic Form
class ProcessForm(FormView):
    """ This Form class create and process a dynamic form based on input.
        It handles all of the model forms from Inventory app.
    """
    template_name = 'inventory/process_form.html'
    product_id =None
    product_type =None
    form_type = 'Suppliers'

    def get_success_url(self):
        """This direct redirect to given url after successfully submitting form
        :return (Method) reverse :
        """
        # todo delete after dubugging
        print("ProcessForm.get_success_url\npk : {}\nproduct_type: {}".format(self.product_id, self.product_type))
        if self.request.GET.get('select') != self.form_type:
            return reverse('inventory-form', kwargs={'pk': self.product_id,
                                                   'product_type': self.product_type})
        else:
            return reverse_lazy('product-home')

    def get_form_class(self):
        """ This method create form_class based on the value of "select" from html
        :return (ModelForm) form_class:
        """
        form_type = self.request.GET.get('select')
        forms_obj = ProductAddForm(form_type)
        return forms_obj.form_class

    def form_valid(self, form):
        """

        :param form:
        :return:
        """
        product_obj = form.save()
        self.product_id = product_obj.product_id
        self.product_type = product_obj.get_classname()

        product_obj.save()

        return super(ProcessForm, self).form_valid(form)


class InventoryForm(FormView):
    template_name = 'inventory/process_form.html'
    success_url = reverse_lazy('product-home')

    def get_product_detail(self):
        """This method will fetch the product_id(pk) and product_type from url kwargs. product_type is being used
        to get content_type_id which is needed to create a generic relation between inventory and
        products(top, bottom, accessories )
        Variables:
            product_type (str): product type name (similar to model).
            product_id (int) : primary key of product
        :return (tuple) product_type, product_id, content_type_id
        """
        product_type = self.kwargs.get('product_type')
        product_id = self.kwargs.get('pk')

        # getting primary key from of content_type
        content_type = ContentType.objects.get(model__iexact=product_type)
        content_type_id = content_type.pk
        return product_type, product_id, content_type_id

    def get_initial(self):

        # You need following fields prepopulated 1: Content_type_id 2: product_id 3
        product_type, product_id, content_type_id = self.get_product_detail()

        initial = super().get_initial()
        initial['product_id'] = product_id
        initial['content_type_id'] = content_type_id

        return initial

    def get_form_class(self, **kwargs):
        return InventoryAddForm

    def form_valid(self, form):
        """
            Inventory have genaric relation to Top, Bottoms, accessories and Shoes Table.
            This method will fetch product_type from url kwargs and product_id which
            will be used to get content_type_id from django_content_type to be used in Inventory


        :param form:
        :return:
        """

        _ , _ , content_type_id = self.get_product_detail()


        inventory_obj = form.save(commit=False)
        print(content_type_id)
        inventory_obj.added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        inventory_obj.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        inventory_obj.content_type_id = content_type_id
        inventory_obj.save()

        return super(InventoryForm, self).form_valid(form)














# Example views and forms for testing purposes

class TestClass(TemplateView):
    template_name = 'inventory/testclass.html'


class TestForms(FormView):
    template_name = 'inventory/testprocessform.html'
    success_url = reverse_lazy('test')

    def get_prefix(self):
        return 'product_form'

    def get_form_class(self):

        form_type = self.request.GET.get('select')
        forms_obj = ProductAddForm(form_type)
        return forms_obj.form_class

    def form_valid(self, form):
        print( self.prefix)
        print('-'*40)
        print(form)
        print('-' * 40)
        print(form.cleaned_data)
        print('-' * 40)
        print(self.kwargs)

        return super(TestForms, self).form_valid(form)