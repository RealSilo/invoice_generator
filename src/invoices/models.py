from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from invoices.choices import *

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    sender = models.CharField(max_length=127)
    receiver = models.CharField(max_length=127)
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True)
    date = models.DateField()
    due_date = models.DateField()
    payment_term = models.CharField(
        max_length=2,
        choices=PAYMENT_TERMS_CHOICES,
        default=UPON_RECEIPT,
    )
    discount_type = models.CharField(
        max_length = 1,
        choices=DISCOUNT_TYPE_CHOICES,
        default=PERCENT,
    )
    discount = models.IntegerField(
        default=0,
    )
    tax_type = models.CharField(
        max_length=1,
        choices=TAX_TYPE_CHOICES,
        default=PERCENT,
    )
    tax = models.IntegerField(
        default=0,
    )
    shipping_price = models.IntegerField(
        default=0,
    )
    subtotal = models.IntegerField(
        default=0,
    )
    total = models.IntegerField(
        default=0
    )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp  = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.receiver

    def get_absolute_url(self):
        return reverse('invoices:detail', kwargs={'id': self.id})

    def get_edit_url(self):
        return reverse('invoices:edit', kwargs={'id': self.id})

    def clean(self):
        if self.date > self.due_date:
            raise ValidationError('Date cannot precede due date')

    def calculate_discount(self, total, discount, discount_type):
        if discount > 0:
            if discount_type == '%':
                total = round(total - (total * discount / 100))
            else:
                total -= discount

        return total

    def calculate_tax(self, total, tax, tax_type):
        if tax > 0:
            if tax_type == '%':
                total = round(total + (total * tax / 100))
            else:
                total += tax
        
        return total

class InvoiceLineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
