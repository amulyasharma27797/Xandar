from django.urls import path
from . import views
app_name = 'products'
urlpatterns = [
    path('<slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/<int:pk>', views.product_add_wishlist_cart, name='product_add'),
]