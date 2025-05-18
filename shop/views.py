from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Category, Order, OrderItem, Wishlist, ProductReview
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_currency_context(request):
    currency = request.GET.get('currency')
    if currency:
        request.session['currency'] = currency
    currency = request.session.get('currency', 'USD')
    # Simple conversion rates for demo (should use real rates in production)
    rates = {'USD': 1, 'EUR': 0.92, 'PKR': 278}
    symbols = {'USD': '$', 'EUR': '€', 'PKR': '₨'}
    rate = rates.get(currency, 1)
    symbol = symbols.get(currency, '$')
    return currency, rate, symbol

def product_list(request):
    currency, rate, symbol = get_currency_context(request)
    products = Product.objects.filter(variation=True)  # Only show admin-enabled variations
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=float(min_price) / rate)
    if max_price:
        products = products.filter(price__lte=float(max_price) / rate)
    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)
    size = request.GET.get('size')
    if size:
        products = products.filter(size=size)
    color = request.GET.get('color')
    if color:
        products = products.filter(color=color)
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_products = Product.objects.all()
    unique_sizes = sorted(set(filter(None, all_products.values_list('size', flat=True))))
    unique_colors = sorted(set(filter(None, all_products.values_list('color', flat=True))))
    # Convert product prices for display
    for p in page_obj:
        p.display_price = round(p.price * rate, 2)
    return render(request, 'product_list.html', {
        'products': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'page_obj': page_obj,
        'unique_sizes': unique_sizes,
        'unique_colors': unique_colors,
        'currency': currency,
        'currency_symbol': symbol,
    })

@require_POST
def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + int(request.POST.get('quantity', 1))
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')
    products = Product.objects.filter(id__in=cart.keys())
    if request.method == 'POST':
        # Validate delivery info before payment step
        if not request.POST.get('confirm_payment'):
            delivery_address = request.POST.get('delivery_address', '').strip()
            contact_email = request.POST.get('contact_email', '').strip()
            contact_phone = request.POST.get('contact_phone', '').strip()
            errors = []
            if not delivery_address:
                errors.append('Delivery address is required.')
            if not contact_email:
                errors.append('Contact email is required.')
            if not contact_phone:
                errors.append('Contact phone is required.')
            if errors:
                cart_items = []
                total = 0
                for product in products:
                    quantity = cart[str(product.id)]
                    subtotal = product.price * quantity
                    total += subtotal
                    cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
                return render(request, 'checkout.html', {
                    'cart_items': cart_items,
                    'total': total,
                    'errors': errors,
                })
            # Store delivery info in session for payment step
            request.session['checkout_info'] = {
                'delivery_address': delivery_address,
                'contact_email': contact_email,
                'contact_phone': contact_phone,
            }
            cart_items = []
            total = 0
            for product in products:
                quantity = cart[str(product.id)]
                subtotal = product.price * quantity
                total += subtotal
                cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total, 'mock_payment': True})
        # Payment confirmation step
        checkout_info = request.session.get('checkout_info', {})
        order = Order.objects.create(
            user=request.user,
            status='paid',
            delivery_address=checkout_info.get('delivery_address', ''),
            contact_email=checkout_info.get('contact_email', ''),
            contact_phone=checkout_info.get('contact_phone', ''),
        )
        for product in products:
            quantity = cart[str(product.id)]
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        request.session['cart'] = {}
        request.session.pop('checkout_info', None)
        return render(request, 'checkout.html', {'order': order, 'success': True})
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def product_detail(request, slug):
    from .views import get_currency_context
    product = get_object_or_404(Product, slug=slug)
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if comment:
            ProductReview.objects.create(product=product, user=request.user, rating=rating, comment=comment)
            return redirect(request.path)
    # AJAX filter logic
    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')
    currency, rate, symbol = get_currency_context(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and filter_type and filter_value:
        # Always return all variations for this product's category
        variations = Product.objects.filter(category=product.category)
        variation_list = [
            {
                'id': p.id,
                'name': p.name,
                'slug': p.slug,
                'size': p.size,
                'color': p.color,
                'price': str(round(p.price * rate, 2)),
                'image_url': p.get_image() if hasattr(p, 'get_image') else (p.image.url if p.image else ''),
            }
            for p in variations
        ]
        return JsonResponse({'success': True, 'variations': variation_list})
    # Normal page render
    suggested_products = product.category.products.exclude(id=product.id)[:4]
    return render(request, 'product_detail.html', {
        'product': product,
        'currency_symbol': symbol,
        'suggested_products': suggested_products,
    })

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_add(request, product_id):
    from .models import Product
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def wishlist_remove(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')

@receiver(post_save, sender=Order)
def award_loyalty_points(sender, instance, created, **kwargs):
    if created and instance.status == 'paid':
        profile, _ = Profile.objects.get_or_create(user=instance.user)
        profile.loyalty_points += int(instance.items.count() * 10)  # 10 points per item
        profile.save()

@receiver(post_save, sender=Order)
def order_email_marketing(sender, instance, created, **kwargs):
    if created and instance.status == 'paid':
        send_mail(
            subject=f"Thank you for your order #{instance.id}",
            message="We appreciate your business! Stay tuned for offers.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=True,
        )
