from django.contrib import admin
from .models import Address, CartItem, Category, Coupon, Order, OrderItem, Product, Review, WishlistItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'brand')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register([Address, CartItem, Coupon, Order, OrderItem, Review, WishlistItem])
