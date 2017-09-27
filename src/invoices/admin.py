from django.contrib import admin

# Register your models here.
from .models import Invoice

class InvoiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "updated", "timestamp")
    list_filter = ("updated", "timestamp")
    class Meta:
        model = Invoice

admin.site.register(Invoice, InvoiceModelAdmin)
