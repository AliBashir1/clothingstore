from django.db import models
from .productdesc import ProductCategory, Size
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_count = models.IntegerField(default=0)
    product_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    added_at = models.DateTimeField()
    updated_at = models.DateTimeField()

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


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=200)
    contact_firstName = models.CharField(max_length=200)
    contact_lastName = models.CharField(max_length=200)
    contact_title = models.CharField(max_length=200)
    supplier_address1 = models.CharField(max_length=200)
    supplier_address2 = models.CharField(max_length=200, null=True)
    supplier_city = models.CharField(max_length=200)
    supplier_state = models.CharField(max_length=2)  # todo find a library to handle state choices
    supplier_country = models.CharField(max_length=200)
    supplier_email = models.EmailField()
    supplier_website = models.URLField()
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwarg):
        self.slug = slugify(self.supplier_name)
        super(Suppliers, self).save(*args, **kwarg)

    def __str__(self):
        return self.supplier_name

    class Meta:
        verbose_name_plural = db_table = 'suppliers'
        verbose_name = 'supplier'

    def get_absolute_url(self):
        return reverse(viewname='supplier-detail', kwargs={'pk': self.id})


class ProductAbstract(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_sku = models.CharField(max_length=50,
                                   unique=True,
                                   db_index=True
                                   )
    product_name = models.CharField(max_length=50)
    product_color = models.CharField(max_length=50)
    product_shortDesc = models.CharField(max_length=50, blank=True)
    product_longDesc = models.CharField(max_length=50, blank=True)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    product_weight = models.DecimalField(max_digits=6, decimal_places=2, default=0)
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
        # verbose_name_plural = db_table =
        # verbose_name = 'bottom'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.product_id})


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
    product_type = models.CharField(max_length=2, default=ProductCategory.Accessories.choices)
    product_image = models.ImageField(upload_to='accessories/')

    class Meta:
        verbose_name_plural = db_table = 'accessories'
        verbose_name = 'accessory'
