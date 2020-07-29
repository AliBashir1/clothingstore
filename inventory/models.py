from django.db import models
from .productdesc import ProductCategory, Size
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from homepage.validators import (alphabets, alphanumeric,
                                 emailvalidator, numeric,
                                 httpurlvalidator, min_value,
                                 alphanumspecial)


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_count = models.IntegerField(default=0, validators=[numeric, min_value])
    product_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[numeric, min_value])
    added_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    # Generic Relaton
    # model type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # product id of model
    product_id = models.PositiveIntegerField()
    # model's object
    content_object = GenericForeignKey(ct_field='content_type', fk_field='product_id')

    class Meta:
        verbose_name_plural = db_table = 'inventory'
        verbose_name = 'inventory'

    # def get_absolute_url(self):
    #     return reverse('product-home',  kwargs={'slug': self.slug})


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=200, validators=[alphabets])
    contact_firstName = models.CharField(max_length=200, validators=[alphabets])
    contact_lastName = models.CharField(max_length=200, validators=[alphabets])
    contact_title = models.CharField(max_length=200, validators=[alphanumspecial])
    supplier_address1 = models.CharField(max_length=200, validators=[alphanumeric])
    supplier_address2 = models.CharField(max_length=100, null=True, blank=True, validators=[alphanumeric])
    # todo find a library to handle state/country choices
    supplier_city = models.CharField(max_length=200)
    supplier_state = models.CharField(max_length=2)
    supplier_country = models.CharField(max_length=200)

    supplier_email = models.EmailField(validators=[emailvalidator])
    supplier_website = models.URLField(validators=[httpurlvalidator])
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwarg):
        self.slug = slugify(self.supplier_name + '_name_' + self.contact_firstName + '_' + self.contact_lastName )
        super(Suppliers, self).save(*args, **kwarg)

    def __str__(self):
        return self.supplier_name

    class Meta:
        verbose_name_plural = db_table = 'suppliers'
        verbose_name = 'supplier'

    def get_absolute_url(self):
        return reverse(viewname='supplier-detail', kwargs={'slug': self.slug})


class ProductAbstract(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_sku = models.CharField(max_length=50, unique=True,
                                   db_index=True, validators=[alphanumeric]
                                   )
    product_name = models.CharField(max_length=50, validators=[alphabets])
    product_color = models.CharField(max_length=50, validators=[alphabets])
    product_shortDesc = models.CharField(max_length=50, blank=True, validators=[alphanumspecial])
    product_longDesc = models.CharField(max_length=50, blank=True, validators=[alphanumspecial])
    product_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[min_value])
    slug = models.SlugField(unique=True, null=False, blank=False)
    # FK
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, default=-1)

    # inventory "Foreign key" reverse relation to generic key
    # since default name for object_id and content type have been used you dont have to specify here
    # if different name been used. it will be required to used here as well

    inventory = GenericRelation(Inventory,
                                related_query_name='product',
                                object_id_field='product_id',
                                content_type_field='content_type')

    def save(self, *args, **kwarg):
        self.slug = slugify(self.product_name + '_' + self.product_sku)
        # todo delete this
        super(ProductAbstract, self).save(*args, **kwarg)

    def __str__(self):
        return self.product_name

    # use it when you start using slug

    def get_classname(self):
        return self.__class__.__name__

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('product-detail',  kwargs={'product_type': self.get_classname(),
                                                  'slug': self.slug })


class Shoes(ProductAbstract):
    product_image = models.ImageField(upload_to='Shoes')
    product_size = models.CharField(max_length=2, choices=Size.ShoeSize.choices, default='NA')

    class Meta:
        verbose_name_plural = db_table = 'shoes'
        verbose_name = 'shoe'


class Tops(ProductAbstract):
    product_type = models.CharField(max_length=2, choices=ProductCategory.TopType.choices)
    product_size = models.CharField(max_length=2,
                                    choices=Size.ClothSize.choices,
                                    default='NA'
                                    )
    product_image = models.ImageField(upload_to='Tops/')

    class Meta:
        verbose_name_plural = db_table = 'tops'
        verbose_name = 'top'


class Bottoms(ProductAbstract):
    product_type = models.CharField(max_length=2,
                                    choices=ProductCategory.BottomType.choices,
                                    default='NA'
                                    )
    product_size = models.CharField(max_length=2,
                                    choices=Size.ClothSize.choices,
                                    default='NA'
                                    )

    product_image = models.ImageField(upload_to='Bottoms/')

    class Meta:
        verbose_name_plural = db_table = 'bottoms'
        verbose_name = 'bottom'


class Accessories(ProductAbstract):

    product_type = models.CharField(max_length=2, default=ProductCategory.Accessories.DEFAULT)
    product_image = models.ImageField(upload_to='accessories/')

    class Meta:
        verbose_name_plural = db_table = 'accessories'
        verbose_name = 'accessory'


"""
Import links:

Drop Down state-country 
link: https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
"""