from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductCategory:

    class TopType(models.TextChoices):

        TEE = 'TE', _('Tee')
        SHIRT = 'SH', _('Shirt')
        TANKTOP = 'TT', _('Tank Top')
        HOODY = 'HO', _('Hoody')
        KURTA = 'KR', _('Kurta')

    class BottomType(models.TextChoices):

        PANTS = 'PA', _('Pants')
        PAJAMA = 'PJ', _('Pajama')
        SHORTS = 'SO', _('Shorts')

    class Accessories(models.TextChoices):
        DEFAULT = 'AC', _('accessories')


class Size:

    class ShoeSize(models.TextChoices):

        FIVE = '5', _('5')
        SIX = '6', _('6')
        SEVEN = '7', _('7')
        EIGHT = '8', _('8')
        NINE = '9', _('9')
        TEN = '10', _('10')
        ELEVEN = '11', _('11')
        TWELVE = '12', _('12')
        THIRTEEN = '13', _('13')

    class ClothSize(models.TextChoices):

        EXTRASMALL = 'XS', _('Extra Small')
        SMALL = 'SM', _('Small')
        MEDIUM = 'MD', _('Medium')
        LARGE = 'LG', _('Large')
        EXTRALARGE = 'XL', _('Extra Large')

    class PantsSize(models.TextChoices):
        pass
