from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from .managers import PropertyPublishedManager

import string
import random

User = get_user_model()


class AdvertType(models.TextChoices):
    FOR_SALE = 'For sale', _('For sale')
    FOR_RENT = 'For rent', _('For rent')
    FOR_AUCTION = 'For auction', _('For auction')


class PropertyType(models.TextChoices):
    HOUSE = 'House', _('House')
    APARTMENT = 'Apartment', _('Apartment')
    OFFICE = 'Office', _('Office')
    WAREHOUSE = 'Warehouse', _('Warehouse')
    OTHER = 'Other', _('Other')


class Property(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("Agent,Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(verbose_name=_('Property Title'), max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    ref_code = models.CharField(verbose_name=_('Property Reference Code'), max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), default='Default Description')
    country = CountryField(verbose_name=_('Country'), default='BD', blank_label='Select Country', help_text='Select Country')
    city = models.CharField(verbose_name=_('City'), max_length=120, default='Dhaka')
    postal_code = models.CharField(verbose_name=_('Postal Code'), default='', max_length=255)
    street_address = models.CharField(verbose_name=_('Stree Address'), default='', max_length=255)
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )
    property_number = models.IntegerField(verbose_name=_('Property Number'), validators=[MinValueValidator(1)], default=999)
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.15,
        help_text="property tax charged",
    )
    total_floors = models.IntegerField(verbose_name=_('Total Floors'), default=0)
    bedrooms = models.IntegerField(verbose_name=_('Bedrooms'), default=0)
    bathrooms = models.IntegerField(verbose_name=_('Bathrooms'), default=0)
    advert_type = models.CharField(
        verbose_name=_('Advertise Type'),
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
        max_length=255
    )
    property_type = models.CharField(
        verbose_name=_('Prpperty type'),
        choices=PropertyType.choices,
        default=PropertyType.OTHER,
        max_length=255
    )
    cover_photo = models.ImageField(
        verbose_name=_('Cover Image'),
        default='/property/default.png',
        null=True,
        blank=True
    )
    photo1 = models.ImageField(
        verbose_name=_('Interior Photo 1'),
        default='/property/default1.png',
        null=True,
        blank=True
    )
    photo2 = models.ImageField(
        verbose_name=_('Interior Photo 2'),
        default='/property/default2.png',
        null=True,
        blank=True
    )
    photo3 = models.ImageField(
        verbose_name=_('Interior Photo 3'),
        default='/property/default3.png',
        null=True,
        blank=True
    )
    photo4 = models.ImageField(
        verbose_name=_('Interior Photo 4'),
        default='/property/default4.png',
        null=True,
        blank=True
    )
    published_status = models.BooleanField(verbose_name=_('Published Status'), default=False)
    views = models.IntegerField(verbose_name=_('Total Views'), default=0)
    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return f'{self.title.title()}'

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)

    @property
    def final_price(self):
        return self.price+round((self.price*self.tax), 2)


class PropertyView(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name='IP Address', max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_views')

    def __str__(self):
        return f'Total views on {self.property.title} is -{self.property.views}'

    class Meta:
        verbose_name = 'Property View'
        verbose_name_plural = 'Property views'
