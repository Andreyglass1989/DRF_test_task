from django.forms import ImageField
from rest_framework import serializers
from Product.models import Product, ArchiveImageProduct
from django.contrib.auth.models import User

from django.conf import settings




class ArchiveImageProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True)
    
    class Meta:
        model = ArchiveImageProduct
        fields=['image', 'product']

    # def to_representation(self, instance):
        # url = instance.image.url
        # request = self.context.get('request', None)
        # if request is not None:
            # return request.build_absolute_uri(url)
        # return url




class ProductSerializer(serializers.ModelSerializer):
    images = ArchiveImageProductSerializer(many=True, read_only=False, required=False)
    
    class Meta:
        model = Product
        fields=('ProductId', 'name', 'price', 'image', 'author', 'images', 'date_create')

    # def create(self, validated_data):
    #     print(validated_data)
    #     images_data = validated_data.pop('images')
    #     product = super().create(validated_data) #Product.objects.create(**validated_data)
    #     for image_data in images_data:
    #         image_data['images'] = product
    #         ArchiveImageProduct.objects.create(**image_data)
    #     return product