from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='home'), path('products/', views.product_list, name='product_list'), path('products/<slug:slug>/', views.product_detail, name='product_detail'), path('bag/', views.cart, name='cart'), path('bag/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'), path('bag/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'), path('wishlist/', views.wishlist, name='wishlist'), path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'), path('checkout/', views.checkout, name='checkout'), path('orders/', views.my_orders, name='my_orders'), path('orders/<int:order_id>/', views.order_detail, name='order_detail')]
