from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import InvoiceForm, InvoiceLineItemFormSet
from .models import Invoice, InvoiceLineItem

def invoice_create(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise Http404

    invoice = Invoice(user = request.user)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        invoice_line_item_formset = InvoiceLineItemFormSet(
            request.POST,
            instance=invoice
        )
        if form.is_valid() and invoice_line_item_formset.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()

            invoice_line_items = []

            for invoice_line_item_form in invoice_line_item_formset:
                name = invoice_line_item_form.cleaned_data.get('name')
                price = invoice_line_item_form.cleaned_data.get('price')
                quantity = invoice_line_item_form.cleaned_data.get('quantity')

                if name and quantity and price:
                    invoice_line_items.append(
                        InvoiceLineItem(
                            invoice = invoice,
                            name = name,
                            quantity = quantity,
                            price = price,
                            amount= price * quantity
                        )
                    )
            try:
                with transaction.atomic():
                    InvoiceLineItem.objects.filter(invoice=invoice).delete()
                    InvoiceLineItem.objects.bulk_create(invoice_line_items)

            except IntegrityError:
                messages.error(request, 'There was an error saving the invoice.')

                return render(
                    request,
                    'invoice_form.html',
                    {'form': form, 'invoice_line_item_formset': invoice_line_item_formset}
                )


            line_item_prices = 0
            for item in invoice_line_items:
                line_item_prices += item.amount
            invoice.subtotal = line_item_prices

            total = invoice.subtotal
            total = invoice.calculate_discount(total, invoice.discount, invoice.discount_type)
            total = invoice.calculate_tax(total, invoice.tax, invoice.tax_type)
            total += invoice.shipping_price

            invoice.total = total
            invoice.save()

            messages.success(request, 'Invoice successfully created')
            return HttpResponseRedirect(invoice.get_absolute_url())
    else:
        form = InvoiceForm(instance=invoice)
        invoice_line_item_formset = InvoiceLineItemFormSet(instance=invoice)

    return render(
        request,
        'invoice_form.html',
        {'form': form, 'invoice_line_item_formset': invoice_line_item_formset}
    )

def invoice_detail(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)

    if not request.user == invoice.user or not request.user.is_superuser:
        raise Http404

    line_items = invoice.invoicelineitem_set.all()

    return render(request, 'invoice_detail.html', {'invoice': invoice, 'line_items': line_items})

def invoice_list(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise Http404

    invoice_list = Invoice.objects.filter(user_id=request.user.id).order_by("-timestamp")
    
    paginator = Paginator(invoice_list, 5)
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)

    return render(request, 'invoice_list.html', {'invoices': invoices})

def invoice_update(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)

    if not request.user == invoice.user or not request.user.is_superuser:
        raise Http404
    
    form = InvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        messages.success(request, 'invoice successfully updated')
        return HttpResponseRedirect(invoice.get_absolute_url())

    return render(request, 'invoice_form.html', {'invoice': invoice, 'form': form})

def invoice_delete(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)

    if not request.user == invoice.user or not request.user.is_superuser:
        raise Http404
    
    invoice.delete()
    messages.success(request, 'invoice successfully deleted')
    return redirect('invoices:list')
