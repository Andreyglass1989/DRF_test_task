from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views



urlpatterns = [
    # base View,
    path('product/', views.productApi),
    path('product/<int:id>/', views.productApi),
    path('arch_image_product/', views.archiveImageProductApi),
    path('arch_image_product/<int:name_image>/', views.archiveImageProductApi),
    path('arch_image_product/savefile', views.saveFile),
   
    # class APIView
    path('product_api/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('product_api/create/', views.ProductListCreateAPIView.as_view()),
    path('product_api/update/<int:pk>/', views.ProductUpdateAPIView.as_view()),
    path('product_api/delete/<int:pk>/', views.ProductDeleteAPIView.as_view()),

    path('product_archiveimage_api/<int:pk>/', views.ArchiveImageProductDetailAPIView.as_view()),
    path('product_archiveimage_api/create/', views.ArchiveImageProductListCreateAPIView.as_view()),
    path('product_archiveimage_api/update/<int:pk>/', views.ArchiveImageProductUpdateAPIView.as_view()),
    path('product_archiveimage_api/delete/<int:pk>/', views.ArchiveImageProductDeleteAPIView.as_view()),

    # MixinView
    # path('product_api_mixin/list/', views.ProductMixinView.as_view()),
    path('product_api_mixin/detail/<int:pk>/', views.ProductMixinView.as_view()),
    path('product_api_mixin/create/', views.ProductMixinView.as_view()),
    path('product_api_mixin/update/<int:pk>/', views.ProductMixinView.as_view()),
    path('product_api_mixin/delete/<int:pk>/', views.ProductMixinView.as_view()),

    # path('product_archiveimage_mixin/list/', views.ArchiveImageProductMixinView.as_view()),
    path('product_archiveimage_mixin/detail/<int:pk>/', views.ArchiveImageProductMixinView.as_view()),
    path('product_archiveimage_mixin/update/<int:pk>/', views.ArchiveImageProductMixinView.as_view()),
    path('product_archiveimage_mixin/create/', views.ArchiveImageProductMixinView.as_view()),
    path('product_archiveimage_mixin/delete/<int:pk>/', views.ArchiveImageProductMixinView.as_view()),


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)