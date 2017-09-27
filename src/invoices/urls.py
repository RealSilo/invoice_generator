from django.conf.urls import url
from django.contrib import admin

from .views import (invoice_list, invoice_detail, invoice_create, invoice_update, invoice_delete)

urlpatterns = [
  url(r'^$', invoice_list, name='list'),
  url(r'^new/$', invoice_create, name='create'),
  url(r'^(?P<id>\d+)/$', invoice_detail, name='detail'),
  url(r'^(?P<id>\d+)/edit/$', invoice_update, name='edit'),
  url(r'^(?P<id>\d+)/delete/$', invoice_delete, name='delete')
]
