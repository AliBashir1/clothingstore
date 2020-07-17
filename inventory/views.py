
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import path, re_path, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView, UpdateView
from .models import Shoes, Tops, Bottoms, Accessories, Suppliers, Inventory
from django.views.generic.edit import FormMixin
from .forms import  InventoryAddForm, ProductAddForm
from datetime import datetime
from django.contrib.contenttypes.models import ContentType


class ProductList(ListView):
    template_name = 'inventory/product_list.html'

    queryset = Shoes.objects.all()
    queryset.extra_context = Tops.objects.all()
    print(queryset)

    # # set the pages for every 2 article and use if is_paginated in template
    # paginate_by = 2
    #
    # def get_ordering(self):
    #     return self.model.product_category
    # def get_context_data(self, **kwargs):
    #     context = super(ShoesList, self).get_context_data(**kwargs)
    #     context['range'] =range(context['paginator'].num_pages)
    #     return context


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
    success_url = reverse_lazy('product-update')

    def get_form_class(self, instance=None):
        """ This method create form_class based on the value of "select" from html
        :return (ModelForm) form_class:
        """
        form_type = self.kwargs.get('product_type')
        forms_obj = ProductAddForm(form_type, instance=instance)
        self.form_class = forms_obj.form_class
        # TODO delete this
        print("form_type: {}\nform_obj: {}\nform_class: {}".format(form_type, forms_obj, self.form_class))
        return self.form_class

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        product_type = self.kwargs.get('product_type')
        model = self.models_mapping.get(product_type)
        # TODO -- delete this
        print("id: {}\nproduct_type: {}\nmodel: {}".format(id, product_type, model))
        return get_object_or_404(klass=model, product_id=id)

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['product_form'] = self.get_form_class(instance=obj)

        # only Products need inventory detail - find a better way to deal with this
        if self.kwargs.get('product_type') != 'Suppliers':
            inv_obj = Inventory.objects.filter()
            context['inventory_form'] = InventoryAddForm(instance=inv_obj)
        return context

    def form_valid(self, form):
        """
         overriding form_valid to add inventory of product
        :param form:
        :return:
        """
        obj = form.save()
        model = ContentType.objects.get(model__iexact=obj.get_classname())
        Inventory.objects.create(product_id=obj.product_id,
                                 product_count=self.request.POST.get('product_count'),
                                 product_cost=self.request.POST.get('product_cost'),
                                 # Date format 2014-07-05 14:34:14
                                 updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 content_type_id=model.pk)

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
    success_url = reverse_lazy('product-home')

    def get_form_class(self):
        """ This method create form_class based on the value of "select" from html
        :return (ModelForm) form_class:
        """
        form_type = self.request.GET.get('select')
        forms_obj = ProductAddForm(form_type)
        return forms_obj.form_class

    def get_context_data(self, **kwargs):
        context = super(ProcessForm, self).get_context_data(**kwargs)
        context['product_form'] = self.get_form_class()
        # only Products need inventory detail - find a better way to deal with this
        if self.request.GET.get('select') != 'Suppliers':
            context['inventory_form'] = InventoryAddForm
        return context

    def form_valid(self, form):
        """
         overriding form_valid to add inventory of product
        :param form:
        :return:
        """
        obj = form.save()
        model = ContentType.objects.get(model__iexact=obj.get_classname())
        Inventory.objects.create(product_id=obj.product_id,
                                 product_count=self.request.POST.get('product_count'),
                                 product_cost=self.request.POST.get('product_cost'),
                                 # Date format 2014-07-05 14:34:14
                                 added_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 content_type_id=model.pk)

        return super(ProcessForm, self).form_valid(form)














# Example views and forms for testing purposes

class TestClass(UpdateView):
    model = Accessories
    fields = '__all__'
    template_name = 'inventory/testclass.html'



class TestForms(FormMixin, TemplateView):
    template_name = 'inventory/testclass.html'
    success_url = reverse_lazy('test')

    def get(self, request, *args, **kwargs):
        if request == 'GET':
            self.get_template_names()
        super(TestForms, self).get(request, *args, **kwargs)

    def get_template_names(self):
        self.template_name = 'inventory/testclass.html'
        return self.template_name

    def get_form_class(self):
        form_class = None
        form_type = self.request.GET.get('select')
        print(form_type)
        forms_obj = ProductAddForm(form_type)
        return forms_obj.form_class

    def get_context_data(self, **kwargs):
        context = super(TestForms, self).get_context_data(**kwargs)
        context['form'] = self.get_form_class()
        # only Products need inventory detail
        if self.request.GET.get('select') != 'Suppliers':
            context['inventory'] = InventoryAddForm
        return context

    def form_valid(self, form):
        form.save()
        return super(TestForms, self).form_valid(form)