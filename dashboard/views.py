from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import models
from blog.models import BlogPost
from shop.models import Order, Wishlist, Product

@staff_member_required
def dashboard_home(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    # Admin dashboard stats
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.filter(status='paid').aggregate(
        total=models.Sum(models.F('items__quantity') * models.F('items__product__price'), output_field=models.FloatField())
    )['total'] or 0
    total_products = Product.objects.count()
    total_wishlist = Wishlist.objects.count()
    total_blog_posts = BlogPost.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:10]
    top_products = Product.objects.annotate(total_sold=models.Sum('orderitem__quantity')).order_by('-total_sold')[:5]
    return render(request, 'dashboard_admin.html', {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_products': total_products,
        'total_wishlist': total_wishlist,
        'total_blog_posts': total_blog_posts,
        'recent_orders': recent_orders,
        'top_products': top_products,
    })

@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('dashboard_home')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    cart = request.session.get('cart', {})
    cart_products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    for product in cart_products:
        quantity = cart[str(product.id)]
        cart_items.append({'product': product, 'quantity': quantity})
    return render(request, 'dashboard_home.html', {
        'orders': orders,
        'wishlist_items': wishlist_items,
        'cart_items': cart_items,
    })
