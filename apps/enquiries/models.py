from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel


class Enquiry(TimeStampedUUIDModel):
    name = models.CharField(verbose_name=_('Your name'), max_length=255)
    phone_number = PhoneNumberField(verbose_name=_('Phone number'), default='')
    email = models.EmailField(verbose_name=_('Email'))
    subject = models.CharField(verbose_name=_('Subject'), max_length=500)
    message = models.TextField(verbose_name=_('Message'))

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'


