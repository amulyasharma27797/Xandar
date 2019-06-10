from django.urls import path, include, re_path
from . import views
app_name = 'products'
urlpatterns = [
    re_path(r'^category=(?P<category>\w+)(&&price=(?P<price>\d+)|&&brand=(?P<brand>\w+)|&&color=(?P<color>\w+))*', views.filter_by),
    #re_path(r'^category=(?P<category>\w+)|price=(?P<price>\d+)', views.filter_by),
    #re_path(r'^brand=(?P<brand>\w+)', views.filter_by),
    path('<slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/<int:pk>', views.product_add_wishlist_cart, name='product_add'),

]


"""
from django.urls import path, include, re_path
from . import views
app_name = 'products'
urlpatterns = [
    re_path(r'^(category=(?P<category>\w+)&&price=(?P<price>\d+))', views.filter_by),
    re_path(r'^category=(?P<category>\w+)|price=(?P<price>\d+)', views.filter_by),
    path('<slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/<int:pk>', views.product_add_wishlist_cart, name='product_add'),

]

"""