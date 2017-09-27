from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from .models import Invoice
from .models import InvoiceLineItem

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'date',
            'due_date',
            'discount',
            'discount_type',
            'notes',
            'payment_term',
            'receiver',
            'sender',
            'shipping_price',
            'tax',
            'tax_type',
            'terms'
        ]

class InvoiceLineItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceLineItem
        fields = [
            'name',
            'quantity',
            'price'
        ]

InvoiceLineItemFormSet = inlineformset_factory(
                            Invoice,
                            InvoiceLineItem,
                            form=InvoiceLineItemForm,
                            extra=1
                        )
