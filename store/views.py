from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Product, CartItem, WishlistItem, Order, OrderItem

def home(request):
    products = Product.objects.filter(is_active=True).select_related('category').order_by('-created_at')[:12]
    return render(request, 'store/home.html', {'products': products, 'categories': Category.objects.all()})

def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    if q: products = products.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    if category: products = products.filter(category__slug=category)
    sort = request.GET.get('sort', '')
    if sort == 'price_low': products = products.order_by('price')
    elif sort == 'price_high': products = products.order_by('-price')
    elif sort == 'newest': products = products.order_by('-created_at')
    return render(request, 'store/products.html', {'products': products, 'categories': Category.objects.all(), 'q': q, 'selected_category': category})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    if request.method != 'POST': return redirect('product_list')
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    size = request.POST.get('size', '').strip()
    qty = max(1, min(int(request.POST.get('quantity', 1)), 10))
    item, created = CartItem.objects.get_or_create(user=request.user, product=product, size=size)
    item.quantity = min(item.quantity + qty if not created else qty, max(product.stock, 1))
    item.save()
    messages.success(request, 'Added to your bag.')
    return redirect('cart')

@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum((i.product.sale_price * i.quantity for i in items), Decimal('0.00'))
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST': CartItem.objects.filter(pk=item_id, user=request.user).delete()
    return redirect('cart')

@login_required
def wishlist(request):
    return render(request, 'store/wishlist.html', {'items': WishlistItem.objects.filter(user=request.user).select_related('product')})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created: item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def checkout(request):
    items = list(CartItem.objects.filter(user=request.user).select_related('product'))
    if not items: messages.info(request, 'Your bag is empty.'); return redirect('cart')
    total = sum((i.product.sale_price * i.quantity for i in items), Decimal('0.00'))
    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        if not address: messages.error(request, 'Enter your delivery address.'); return redirect('checkout')
        with transaction.atomic():
            order = Order.objects.create(user=request.user, address_text=address, order_total=total, payment_method='COD')
            for item in items:
                if item.quantity > item.product.stock: messages.error(request, f'Not enough stock for {item.product.name}.'); return redirect('cart')
                OrderItem.objects.create(order=order, product=item.product, product_name=item.product.name, size=item.size, quantity=item.quantity, unit_price=item.product.sale_price)
                item.product.stock -= item.quantity; item.product.save(update_fields=['stock'])
            CartItem.objects.filter(user=request.user).delete()
        send_mail('Your VastraVibe order is confirmed', f'Order #{order.pk}\nTotal: ₹{total}\nPayment: Cash on Delivery', settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=True)
        return redirect('order_detail', order_id=order.pk)
    return render(request, 'store/checkout.html', {'items': items, 'total': total})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    return render(request, 'store/my_orders.html', {'orders': Order.objects.filter(user=request.user).order_by('-created_at')})
