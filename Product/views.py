from cgitb import lookup
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Product import serializers
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from Product.models import *
from Product.serializers import ProductSerializer, ArchiveImageProductSerializer
# Create your views here.

from django.core.files.storage import default_storage
import json
# from django.http import JsonResponse

from rest_framework import status, permissions, generics, mixins
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser, JSONParser





# Function BaseViews //////////////////////////////////////////////////////

@csrf_exempt
def productApi(request, id=None):
    if request.method == "GET":
        if id is not None:
            # detail_view
            # product = Product.objects.filter(ProductId=id)
            # if not product.exists():
            #     raise Http404
            product = get_object_or_404(Product, ProductId=id)
            product_serializer = ProductSerializer(product, many=False)
            return JsonResponse(product_serializer.data)
        else:
            #list_view
            product = Product.objects.all()
            product_serializer = ProductSerializer(product, many=True)
            return JsonResponse(product_serializer.data, safe=False)

    elif request.method == 'POST':
        # create
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid(raise_exception=True):
            name = product_serializer.validated_data.get('name')
            price = product_serializer.validated_data.get('price')
            image = product_serializer.validated_data.get('image') or None
            author = product_serializer.validated_data.get('author')
            date_create = product_serializer.validated_data.get('date_create') 
            if image is None:
                image = ''
            product_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        # return Response({"invalid": "not good data"}, status=400)
        # or
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == "PUT":
        product_data = JSONParser().parse(request)
        product = Product.objects.get(ProductId = product_data['ProductId'])
        product_serializer = ProductSerializer(product, data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse("Update Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)

    elif request.method == "DELETE":
        product = Product.objects.get(ProductId=id)
        product.delete()
        return JsonResponse("Delete Successfully", safe=False)




@csrf_exempt
def archiveImageProductApi(request, name_image=None):

    if request.method == "GET":
        if name_image is not None:
            # print(name_image)
            image_products = get_object_or_404(ArchiveImageProduct, id=name_image)
            image_product_serializer = ArchiveImageProductSerializer(image_products, many=False)
            return JsonResponse(image_product_serializer.data, safe=False)
        else:
            image_products = ArchiveImageProduct.objects.all()
            image_product_serializer = ArchiveImageProductSerializer(image_products, many=True)
            return JsonResponse(image_product_serializer.data, safe=False)

    elif request.method == 'POST':
        print(request)
        image_product = JSONParser().parse(request)
        image_product_serializer = ArchiveImageProductSerializer(data=image_product)
        if image_product_serializer.is_valid():
            image_product_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == "PUT":
        image_product_data = JSONParser().parse(request)
        print(image_product_data, name_image)
        image_product = ArchiveImageProduct.objects.get(id = image_product_data['id'])
        image_product_serializer = ArchiveImageProductSerializer(image_product, data=image_product_data)
        print(image_product_serializer)
        if image_product_serializer.is_valid():
            image_product_serializer.save()
            return JsonResponse("Update Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)

    elif request.method == "DELETE":
        image_product = ArchiveImageProduct.objects.get(id=name_image)
        image_product.delete()
        return JsonResponse("Delete Successfully", safe=False)


@csrf_exempt
def saveFile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name,safe=False)


# //////////////////////////////////////////////////////////////////////////////////




# Class Detail View 
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAccountAdminOrReadOnly]


#Class CreateAPIView
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_class = (FileUploadParser, MultiPartParser)

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        # image = serializer.validated_data.get('image') or None
        author = serializer.validated_data.get('author')
        date_create = serializer.validated_data.get('date_create') 
        serializer.save()
        # Django signal

    # def post(self, request, format=None):
    #         serializer = ProductSerializer(data=request.DATA, files=request.FILES)

    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#class ListApiView & ListCreateAPIView
# class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAccountAdminOrReadOnly]




# UpdateAPIView
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.images:
            instance.images = "" 



# DestroyAPIView
class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)





#Class CreateAPIView Second Model
class ArchiveImageProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = ArchiveImageProduct.objects.all()
    serializer_class = ArchiveImageProductSerializer
    parser_class = (FileUploadParser, MultiPartParser)

# Class Detail View 
class ArchiveImageProductDetailAPIView(generics.RetrieveAPIView):
    queryset = ArchiveImageProduct.objects.all()
    serializer_class = ArchiveImageProductSerializer

# UpdateAPIView
class ArchiveImageProductUpdateAPIView(generics.UpdateAPIView):
    queryset = ArchiveImageProduct.objects.all()
    serializer_class = ArchiveImageProductSerializer
    lookup_field = 'pk'

# DestroyAPIView
class ArchiveImageProductDeleteAPIView(generics.DestroyAPIView):
    queryset = ArchiveImageProduct.objects.all()
    serializer_class = ArchiveImageProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


# ////////////////////////////////////////////////////////////





# MixinView
class ProductMixinView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset         = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field     = 'pk'

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # print(args, kwargs)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # print(serializer.validated_data)
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        # image = serializer.validated_data.get('image') or None
        author = serializer.validated_data.get('author')
        date_create = serializer.validated_data.get('date_create') 
        serializer.save()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)





# MixinView
class ArchiveImageProductMixinView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset         = ArchiveImageProduct.objects.all()
    serializer_class = ArchiveImageProductSerializer
    lookup_field     = 'pk'

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # print(args, kwargs)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
