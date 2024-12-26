from django.urls import include, path
from .import views

urlpatterns = [
    path('', views.ProductListAPIView.as_view(), name = 'ProductListAPIView'),
    path('<int:productId>/', views.ProductDetailAPIView.as_view(), name = 'ProductDetailAPIView')
]
