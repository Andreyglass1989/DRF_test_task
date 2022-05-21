import imp
from django.contrib import admin
from .models import Product, ArchiveImageProduct
# Register your models here.


class ImagesInline(admin.TabularInline):
  model = ArchiveImageProduct

class ProductAdmin(admin.ModelAdmin):
  inlines = [
    ImagesInline,
  ]
  list_display = ('name', 'date_create', )
admin.site.register(Product, ProductAdmin) 