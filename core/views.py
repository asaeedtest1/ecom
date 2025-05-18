from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from dashboard.models import VisitorLog
from shop.models import Product
from blog.models import BlogPost
from core.models import HomeBanner

def home(request):
    # Log visitor IP
    ip = request.META.get('REMOTE_ADDR')
    try:
        VisitorLog.objects.create(ip_address=ip)
    except Exception:
        pass
    banner = HomeBanner.objects.filter(is_active=True).order_by('-updated_at').first()
    featured_products = Product.objects.filter(show_on_homepage=True)[:8]
    featured_blogs = BlogPost.objects.filter(show_on_homepage=True)[:3]
    return render(request, 'home.html', {
        'banner': banner,
        'featured_products': featured_products,
        'featured_blogs': featured_blogs,
    })

def about(request):
    return render(request, 'about.html')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email to site admin (from settings)
            send_mail(
                subject=f"Contact Form: {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )
            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
