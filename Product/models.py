from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ArchiveImageProduct(models.Model):
    id      = models.AutoField(primary_key=True)
    image   = models.ImageField(u'Images', upload_to='static/images_folder', blank=True, null=True)
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)

    def product_name(self):
        return self.product


class Product(models.Model):
    ProductId   = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=250)
    price       = models.DecimalField(max_digits=5, decimal_places=2)
    image       = models.ImageField(u'Images', upload_to='static/images_folder', blank=True, null=True)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)

    def __str__(self):
        return self.name + ' ' + self.date_create.strftime('%d/%m/%y')
