from django.shortcuts import render, reverse, get_object_or_404
from django.urls import path, re_path, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView, UpdateView
from .models import Shoes, Tops, Bottoms, Accessories, Suppliers, Inventory
from django.views.generic.edit import FormMixin, SingleObjectMixin
from .forms import  GetForm
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
        slug = self.kwargs.get('slug')
        product_type = self.kwargs.get('product_type')
        model = self.models_mapping.get(product_type)
        return get_object_or_404(klass=model, slug=slug)


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
    product_id = None
    product_type = None
    slug = None
    form_type = None
    SUPPLIERS = 'Suppliers'
    INVENTORY = 'Inventory'

    def get_product_detail(self):
        product_type = self.kwargs.get('product_type')
        slug = self.kwargs.get('slug')
        model = self.models_mapping.get(product_type)

        return slug, product_type, model

    def get_success_url(self):
        """Method returns success url based on form type
        :return (Method) reverse :
        """
        if self.kwargs.get('product_type'):
            return reverse(viewname='process-inventory-form', kwargs={'product_type': self.product_type,
                                                                      'inventory': self.INVENTORY,
                                                                      'slug': self.slug})
        else:
            return reverse_lazy('product-home')

    def get_form_class(self):
        """This method gets the product type from url which has similar name as model of product.
        That information is being used to get form_class from ProductAddForm.

        :param (Model) instance:
       :return (ModelForm) form_class:
        """

        _, product_type, _ = self.get_product_detail()
        forms_obj = GetForm(product_type)
        # Returns form_class from ProductAddForm
        return forms_obj.form_class

    def get_object(self, queryset=None):
        """Method uses pk(product_id) and product_type from url to get Model and object primary key
        which is used to return current instance.
        :param queryset:
        :return (MODEL) Object:

        """

        slug, product_type, model = self.get_product_detail()
        return get_object_or_404(klass=model, slug=slug)


    def form_valid(self, form):
        """
         overriding form_valid to add inventory of product
        :param form:
        :return:
        """
        instance = form.save()

        # product_id and type are only needed for products
        if self.request.GET.get('select') != self.SUPPLIERS:
            self.product_id = instance.product_id
            self.product_type = instance.get_classname()
            self.slug = instance.slug

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
    """ ProcessForm class handles forms of products and suppliers. form_type used to check if form is of product or
    suppliers.
    """
    SUPPLIERS = 'Suppliers'
    INVENTORY = 'Inventory'

    template_name = 'inventory/process_form.html'
    product_id =None
    content_type_id = None
    product_type =None
    slug=None
    form_type = None

    def _get_product_detail(self):
        models_mapping = {
            'Tops': Tops,
            'Bottoms': Bottoms,
            'Accessories': Accessories,
            'Shoes': Shoes,
            'Suppliers': Suppliers,
        }

        if self.kwargs.get('inventory'):
            self.product_type = self.kwargs.get('product_type')
            self.slug = self.kwargs.get('slug')
            self.model = models_mapping.get(self.product_type)
            product_object = get_object_or_404(klass=self.model, slug=self.slug)

            # Generic Relation - this returns the model object in ContentType table
            content_type= ContentType.objects.get(model__iexact=self.product_type)
            self.content_type_id = content_type.pk
            self.product_id = product_object.product_id

        return self.content_type_id, self.product_id

    def get_success_url(self):
        """Method returns success url based on form type
        :return (Method) reverse :
        """
        if self.request.GET.get('select') and self.request.GET.get('select') != self.SUPPLIERS:
            return reverse(viewname='process-inventory-form', kwargs={
                                                                'product_type': self.product_type,
                                                                'inventory': self.INVENTORY,
                                                                'slug': self.slug
                                                            })
        else:
            return reverse_lazy('product-home')

    def get_form_class(self):
        """ This method create form_class based on the value of "select" from html
        :return (ModelForm) form_class:
        """
        if self.request.GET.get('select'):
            self.form_type = self.request.GET.get('select')

        if self.kwargs.get('inventory'):
            self.form_type = self.INVENTORY

        form_obj = GetForm(product_type=self.form_type)
        return form_obj.form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('select'):
            context['product_type'] = self.request.GET.get('select')
        return context

    def form_valid(self, form):
        """product_id and product_type are only being saved for products which can be used in inventory form
        :param form:
        :return:
        """
        if self.request.GET.get('select'):
            instance = form.save()
            # product_id and type are only needed for products
            if self.request.GET.get('select') != self.SUPPLIERS:
                self.product_id = instance.product_id
                self.product_type = instance.get_classname()
                self.slug = instance.slug

        if self.kwargs.get('inventory'):
            self._get_product_detail()
            inventory_obj = form.save(commit=False)
            inventory_obj.added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inventory_obj.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inventory_obj.content_type_id = self.content_type_id
            inventory_obj.product_id = self.product_id
            inventory_obj.save()

        return super().form_valid(form)

